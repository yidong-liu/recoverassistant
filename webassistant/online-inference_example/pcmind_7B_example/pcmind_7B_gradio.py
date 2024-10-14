"""
在线推理任务配置：
集群：智算GPU
资源：A100,V100
镜像：Llama3（chenzh创建）
模型： (仓库)
启动脚本:
"""

import os
import gradio as gr
from c2net.context import prepare

c2net_context = prepare()
model_path = (
    c2net_context.pretrain_model_path
    + "/PCMind-7B-1T-Transformers"
)

from fastapi import FastAPI
from dataclasses import dataclass, field
from threading import Thread
from typing import Iterable, List, Tuple
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer

import sys

sys.path.append(
    "/tmp/pretrainmodel/PCMind-7B-1T-Transformers"
)

app = FastAPI()
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_path, device_map="auto", trust_remote_code=True
)
terminators = [tokenizer.eos_token_id]

DESCRIPTION = f"""
<div>
<h1 style="text-align: center;">PengCheng-Mind 7B 在线体验</h1>
<p>🔎 此体验界面通过启智社区在线推理任务构建，使用算力网资源部署。</p>
<p>⚙️ 可在下方 `Parameters` 中设置参数，调整模型输出效果：<br>
    1> `Tempurature` 值越大，模型输出不确定性越高；<br>
    2> `Max new tokens` 控制模型最大可生成长度；<br>
    3> `Top p` 值越大，模型输出多样性和随机性；<br>
    4> `Repetition Penalty` 值越大，模型重复同样内容的概率越低；<br>
    5> `System Message` 系统预设指令，你可以设定大模型的人设 </p></p>
</div>
"""

LICENSE = """
<p/>

---
Built with OpenI and C2Net.
"""

PLACEHOLDER = f"""
<div style="padding: 30px; text-align: center; display: flex; flex-direction: column; align-items: center;">
   <h1 style="font-size: 28px; margin-bottom: 2px; opacity: 0.55;">PengCheng-Mind 7B</h1>
   <p style="font-size: 18px; margin-bottom: 2px; opacity: 0.65;">请提问，模型支持 <b>中文</b> 与 <b>英文</b> 输入<br>
</div>
"""

css = """
h1 {
  text-align: center;
  display: block;
}s
#duplicate-button {
  margin: auto;
  color: white;
  background: #1565c0;
  border-radius: 100vh;
}
"""


def streaming_chat(
    message: str,
    history: List[Tuple[str, str]] = [],
    system_message: str = "你是一个聊天助手，你需要用中文回答用户的问题!",
    max_tokens: int = 512,
    temperature: float = 0.7,
    top_p: float = 0.9,
    repetition_penalty: float = 1.0,
) -> Iterable[str]:
    """
    Generate a streaming response using the llama3-8b model.
    """
    conversation = [{"role": "system", "content": system_message}]
    if history is not None:
        for user, assistant in history:
            conversation.extend(
                [
                    {"role": "Human", "content": user},
                    {"role": "Assistant", "content": assistant},
                ]
            )
    conversation.append({"role": "Human", "content": message})
    input_str = ""
    for message_dict in conversation:
        input_str += message_dict["role"] + ": " + message_dict["content"] + "\n "

    """    
    input_ids = tokenizer.apply_chat_template(conversation, return_tensors="pt", add_special_tokens=False).to(
        model.device
    )
    """
    input_ids = tokenizer.encode(
        input_str, return_tensors="pt", add_special_tokens=False
    ).to(model.device)

    streamer = TextIteratorStreamer(
        tokenizer, timeout=10.0, skip_prompt=True, skip_special_tokens=True
    )

    generate_kwargs = dict(
        input_ids=input_ids,
        streamer=streamer,
        do_sample=True,
        max_new_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        eos_token_id=terminators,
    )
    # This will enforce greedy generation (do_sample=False) when the temperature is passed 0, avoiding the crash.
    if temperature == 0:
        generate_kwargs["do_sample"] = False

    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()

    response = ""
    for new_token in streamer:
        if new_token != "":
            response += new_token
            yield response


# Gradio block
chatbot = gr.Chatbot(height=450, placeholder=PLACEHOLDER, label="Gradio ChatInterface")

with gr.Blocks(fill_height=True, css=css) as demo:

    gr.Markdown(DESCRIPTION)

    gr.ChatInterface(
        fn=streaming_chat,
        chatbot=chatbot,
        fill_height=True,
        additional_inputs_accordion=gr.Accordion(
            label="⚙️ Parameters", open=False, render=False
        ),
        additional_inputs=[
            gr.Textbox(
                value="你是一个聊天助手，你需要用中文回答用户的问题!",
                label="System message",
            ),
            gr.Slider(
                minimum=1, maximum=2048, value=512, step=1, label="Max new tokens"
            ),
            gr.Slider(
                minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature"
            ),
            gr.Slider(
                minimum=0.1,
                maximum=1.0,
                value=0.95,
                step=0.05,
                label="Top-p",
            ),
            gr.Slider(
                minimum=0.1,
                maximum=1.0,
                value=0.95,
                step=0.05,
                label="Repetition Penalty",
            ),
        ],
        examples=[
            ["如何在火星上建立人类基地？简短回答。"],
            ["向8岁的我解释相对论。"],
            ["9,000乘以9,000是多少？"],
            ["给我的朋友韩梅梅写一段温馨的生日祝福。"],
            ["辩证为什么小企鹅可能适合当森林之王？"],
        ],
        cache_examples=False,
    )

    gr.Markdown(LICENSE)

demo.queue()
app = gr.mount_gradio_app(
    app,
    demo,
    path=os.getenv("OPENI_SELF_URL"),
    root_path=os.getenv("OPENI_SELF_URL"),
)

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('OPENI_SELF_PORT')))