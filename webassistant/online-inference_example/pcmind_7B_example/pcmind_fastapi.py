"""
在线推理任务配置：
集群：智算GPU
资源：A100、V100
镜像：Llama3（chenzh创建）
模型：PCMind-7B-1T-Transformers(仓库yanghanshuo/Online_inference)
启动脚本: pcmind_fastapi.py
"""

import os

from c2net.context import prepare

model_name = "PCMind-7B-1T-Transformers"
c2net_context = prepare()
model_path = c2net_context.pretrain_model_path + f"/{model_name}"

import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from threading import Thread
from typing import Iterable, List, Optional, Tuple

from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer

sys.path.append(f"/tmp/pretrainmodel/{model_name}/")

tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", trust_remote_code=True)
terminators = [tokenizer.eos_token_id]


@dataclass
class ChatHistory:
    user_message: str
    bot_response: str


@dataclass
class ChatParams:
    message: str
    history: Optional[List[ChatHistory]] = None
    system_message: str = "你是一个聊天助手，你需要用中文回答用户的问题!"
    max_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.9
    repetition_penalty: float = 1.0


def streaming_chat(params: ChatParams) -> Iterable[str]:
    """
    Generate a streaming response using the llama3-8b model.
    """
    conversation = [{"role": "system", "content": params.system_message}]
    if params.history is not None:
        for _chat in params.history:
            conversation.extend(
                [
                    {"role": "Human", "content": _chat.user_message},
                    {"role": "Assistant", "content": _chat.bot_response},
                ]
            )
    conversation.append({"role": "Human", "content": params.message})
    input_str = ""
    for message_dict in conversation:
        input_str += message_dict["role"] + ": " + message_dict["content"] + "\n "

    """    
    input_ids = tokenizer.apply_chat_template(conversation, return_tensors="pt", add_special_tokens=False).to(
        model.device
    )
    """
    input_ids = tokenizer.encode(input_str, return_tensors="pt", add_special_tokens=False).to(model.device)

    streamer = TextIteratorStreamer(tokenizer, timeout=10.0, skip_prompt=True, skip_special_tokens=True)

    generate_kwargs = dict(
        input_ids=input_ids,
        streamer=streamer,
        do_sample=True,
        max_new_tokens=params.max_tokens,
        temperature=params.temperature,
        top_p=params.top_p,
        repetition_penalty=params.repetition_penalty,
        eos_token_id=terminators,
    )
    # This will enforce greedy generation (do_sample=False) when the temperature is passed 0, avoiding the crash.
    if params.temperature == 0:
        generate_kwargs["do_sample"] = False

    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()

    for text in streamer:
        if text:
            yield text


import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse

app = FastAPI()
base_url = os.getenv("OCTOPUS_NOTEBOOK_BASE_URL")

sample_json = """
{
   "message":"我的名字是什么",
   "history":[
      {
         "user_message":"我叫乔治",
         "bot_response":"很高兴认识你，乔治！你来自哪里？有没有任何有趣的事情想和我分享？"
      }
   ],
   "system_message":"你是一个聊天助手，你需要用中文回答用户的问题!",
   "max_tokens":512,
   "temperature":0.7,
   "top_p":0.9,
   "repetition_penalty":1.0
}
"""

desc = f"""
<div>
<h1 style="text-align: left;">PengCheng-Mind 7B 在线推理部署服务</h1>
<p> 请使用下方的<b>🔗链接</b> 与 <b>🔎 JSON参数</b>，发送 <b>POST</b> 请求进行推理。此API将返回流式数据。</p>
<p><b>🔗 POST https://mlunotebook.openi.org.cn{base_url}/chat </b></p>
<p> <b>🔎 示例JSON参数：</b>{sample_json}</div>
"""


@app.get(base_url)
async def home():
    return HTMLResponse(content=desc, status_code=200)


@app.post(f"{base_url}/chat")
async def streaming_chat_api(params: ChatParams):
    return StreamingResponse(
        streaming_chat(params),
        media_type="application/octet-stream; charset=utf-8",
        headers={"X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('OPENI_SELF_PORT')))