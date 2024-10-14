'''只选一个sd xl的模型'''
import gradio as gr
import uvicorn
from fastapi import FastAPI
from io import BytesIO
from datetime import datetime
from generate import ImageRequest
from generate import generate, pipe_init, get_sd_model_dir, translation
from generate import scheduler_mapping
import base64
import datetime
import os
import re

app = FastAPI()

from c2net.context import prepare

#初始化导入数据集和预训练模型到容器内
c2net_context = prepare()

#只选择一个sd xl的diffusers模型
sd_xl_id = get_sd_model_dir(c2net_context.pretrain_model_path)
base_model_id = sd_xl_id
base_model_name = os.path.basename(base_model_id)

#初始化pipe
pipe = pipe_init(base_model_id, "EulerAnc", "text2img", "XL 1.0", False)

base_url = os.getenv('OPENI_SELF_URL')

def infer(prompt, negative, scale, samples=4, width=512, height=512, steps=50, refiner_strength=0.3, seed=-1, scheduler_name="EulerDiscreteScheduler"):

    image_request = ImageRequest(
    prompt=translation(prompt),
    pipeline_name="text2img",
    image_input=None,
    mask_input=None,
    negative_prompt=translation(negative),
    steps=steps,
    width=width,
    height=height,
    guidance_scale=scale,
    enable_attention_slicing=False,
    enable_cpu_offload=False,
    version="XL 1.0",
    strength= refiner_strength,
    seed= seed,
    num_images_per_prompt = samples,
    scheduler_name = scheduler_name
    )

    image_input = None
    mask_input = None

    generated_images = generate(
        image_request.prompt,
        image_request.pipeline_name,
        model_id = base_model_id,
        pipe=pipe,
        image_input=image_input,
        mask_input=mask_input,
        negative_prompt=image_request.negative_prompt,
        steps=image_request.steps,
        width=image_request.width,
        height=image_request.height,
        guidance_scale=image_request.guidance_scale,
        enable_attention_slicing=image_request.enable_attention_slicing,
        enable_cpu_offload=image_request.enable_cpu_offload,
        version=image_request.version,
        strength=image_request.strength,
        seed = image_request.seed,
        num_images_per_prompt = image_request.num_images_per_prompt,
        scheduler_name = image_request.scheduler_name
    )
            
    image_base64_list = []
    for generated_image in generated_images:
        buffered = BytesIO()
        generated_image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        image_b64 = (f"data:image/jpeg;base64,{img_str}")
        image_base64_list.append(image_b64)
        
    return image_base64_list



# Reference: https://huggingface.co/spaces/google/sdxl/blob/main/app.py#L139
css = """
        .gradio-container {
            font-family: 'IBM Plex Sans', sans-serif;
        }
        .gr-button {
            color: white;
            border-color: black;
            background: black;
        }
        input[type='range'] {
            accent-color: black;
        }
        .dark input[type='range'] {
            accent-color: #dfdfdf;
        }
        .gradio-container {
            max-width: 1200px !important;
            margin: auto;
            padding-top: 1.5rem;
        }
        #gallery {
            min-height: 22rem;
            margin-bottom: 15px;
            margin-left: auto;
            margin-right: auto;
            border-bottom-right-radius: .5rem !important;
            border-bottom-left-radius: .5rem !important;
        }
        #gallery>div>.h-full {
            min-height: 20rem;
        }
        .details:hover {
            text-decoration: underline;
        }
        .gr-button {
            white-space: nowrap;
        }
        .gr-button:focus {
            border-color: rgb(147 197 253 / var(--tw-border-opacity));
            outline: none;
            box-shadow: var(--tw-ring-offset-shadow), var(--tw-ring-shadow), var(--tw-shadow, 0 0 #0000);
            --tw-border-opacity: 1;
            --tw-ring-offset-shadow: var(--tw-ring-inset) 0 0 0 var(--tw-ring-offset-width) var(--tw-ring-offset-color);
            --tw-ring-shadow: var(--tw-ring-inset) 0 0 0 calc(3px var(--tw-ring-offset-width)) var(--tw-ring-color);
            --tw-ring-color: rgb(191 219 254 / var(--tw-ring-opacity));
            --tw-ring-opacity: .5;
        }
        #advanced-btn {
            font-size: .7rem !important;
            line-height: 19px;
            margin-top: 12px;
            margin-bottom: 12px;
            padding: 2px 8px;
            border-radius: 14px !important;
        }
        #advanced-options {
            display: none;
            margin-bottom: 20px;
        }
        .footer {
            margin-bottom: 45px;
            margin-top: 35px;
            text-align: center;
            border-bottom: 1px solid #e5e5e5;
        }
        .footer>p {
            font-size: .8rem;
            display: inline-block;
            padding: 10px 10px;
            transform: translateY(10px);
            background: white;
        }
        .dark .footer {
            border-color: #303030;
        }
        .dark .footer>p {
            background: #0b0f19;
        }
        .acknowledgments h4{
            margin: 1.25em 0 .25em 0;
            font-weight: bold;
            font-size: 115%;
        }
        .animate-spin {
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            from {
                transform: rotate(0deg);
            }
            to {
                transform: rotate(360deg);
            }
        }
        #share-btn-container {
            display: flex; padding-left: 0.5rem !important; padding-right: 0.5rem !important; background-color: #000000; justify-content: center; align-items: center; border-radius: 9999px !important; width: 13rem;
            margin-top: 10px;
            margin-left: auto;
        }
        #share-btn {
            all: initial; color: #ffffff;font-weight: 600; cursor:pointer; font-family: 'IBM Plex Sans', sans-serif; margin-left: 0.5rem !important; padding-top: 0.25rem !important; padding-bottom: 0.25rem !important;right:0;
        }
        #share-btn * {
            all: unset;
        }
        #share-btn-container div:nth-child(-n+2){
            width: auto !important;
            min-height: 0px !important;
        }
        #share-btn-container .wrap {
            display: none !important;
        }
        
        .gr-form{
            flex: 1 1 50%; border-top-right-radius: 0; border-bottom-right-radius: 0;
        }
        #prompt-container{
            gap: 0;
            margin: 0 10px 0 0;
        }
        #generate-image-btn {
            margin: 0 0 0 10px;
        }
        #prompt-text-input, #negative-prompt-text-input{padding: .45rem 0.625rem}
        #component-16{border-top-width: 1px!important;margin-top: 1em}
        .image_duplication{position: absolute; width: 100px; left: 50px}
"""

block = gr.Blocks(css=css)

default_guidance_scale = 7
    
examples = [
    [
        '手工制作，充满活力的钩针编织狮子舞服装，复杂的钩针细节，俏皮的面部表情，大大的卡通眼睛和张开的嘴巴，舌头古怪，花卉装饰图案，以白色、金色、红色为主的多彩调色板，蓝色和绿色的点缀，手工制作的美学，纱线材料中明显的蓬松质感，中国文化灵感，节日人物形象，与对比鲜明的蓝绿色背景形成鲜明对比，柔和的灯光凸显了纹理和色彩的活力，散发着文化庆典的迷人奇思妙想。',
        '低质量， jpeg 伪影，模糊，画质差，丑陋，质量最差',
        default_guidance_scale
    ],
    [
        'film grain texture,analog photography aesthetic,Vibrant, whimsical creature costume, bold pink horns, textured turquoise fur, deep-set googly eyes, playful orange fringe reminiscent of a beard, mismatched ear design with an eye motif, fabric blending artistic chaos and craftsmanship, patches of flowery patterns, contrasting sleeves, backdrop in a vivid, uniform yellow enhancing the costumes dramatic colors, creating a sense of joy and eccentricity, handmade aesthetic suggesting a blend of folk art influences and contemporary fantasy elements.,',
        'low quality,jpeg artifacts,blurry,poorly drawn,ugly,worst quality,',
        default_guidance_scale
    ],
]


with block:
    gr.HTML(
        f"""
            <div style="text-align: center; margin: 0 auto;">
              <div
                style="
                  display: inline-flex;
                  align-items: center;
                  gap: 0.8rem;
                  font-size: 1.75rem;
                "
              >
                <svg
                  width="0.65em"
                  height="0.65em"
                  viewBox="0 0 115 115"
                  fill="none"
                >
                  <rect width="23" height="23" fill="white"></rect>
                  <rect y="69" width="23" height="23" fill="white"></rect>
                  <rect x="23" width="23" height="23" fill="#AEAEAE"></rect>
                  <rect x="23" y="69" width="23" height="23" fill="#AEAEAE"></rect>
                  <rect x="46" width="23" height="23" fill="white"></rect>
                  <rect x="46" y="69" width="23" height="23" fill="white"></rect>
                  <rect x="69" width="23" height="23" fill="black"></rect>
                  <rect x="69" y="69" width="23" height="23" fill="black"></rect>
                  <rect x="92" width="23" height="23" fill="#D9D9D9"></rect>
                  <rect x="92" y="69" width="23" height="23" fill="#AEAEAE"></rect>
                  <rect x="115" y="46" width="23" height="23" fill="white"></rect>
                  <rect x="115" y="115" width="23" height="23" fill="white"></rect>
                  <rect x="115" y="69" width="23" height="23" fill="#D9D9D9"></rect>
                  <rect x="92" y="46" width="23" height="23" fill="#AEAEAE"></rect>
                  <rect x="92" y="115" width="23" height="23" fill="#AEAEAE"></rect>
                  <rect x="92" y="69" width="23" height="23" fill="white"></rect>
                  <rect x="69" y="46" width="23" height="23" fill="white"></rect>
                  <rect x="69" y="115" width="23" height="23" fill="white"></rect>
                  <rect x="69" y="69" width="23" height="23" fill="#D9D9D9"></rect>
                  <rect x="46" y="46" width="23" height="23" fill="black"></rect>
                  <rect x="46" y="115" width="23" height="23" fill="black"></rect>
                  <rect x="46" y="69" width="23" height="23" fill="black"></rect>
                  <rect x="23" y="46" width="23" height="23" fill="#D9D9D9"></rect>
                  <rect x="23" y="115" width="23" height="23" fill="#AEAEAE"></rect>
                  <rect x="23" y="69" width="23" height="23" fill="black"></rect>
                <h1 style="font-weight: 900; margin-bottom: 7px;margin-top:5px">
                  {base_model_name}
                </h1>
              </div>
              <p style="margin-bottom: 10px; font-size: 94%; line-height: 23px;">
                在线体验Stable Diffusion  
                <br/>
              </p>
            </div>
        """
    )
    with gr.Row(style={"max-width": "1200px"}):
        with gr.Column(style={"width": "50%"}):
            with gr.Group():
                text = gr.Textbox(
                    label="Enter your prompt",
                    show_label=False,
                    max_lines=10,
                    placeholder="Enter your prompt",
                    elem_id="prompt-text-input",
                ).style(
                    border=(True, False, True, True),
                    rounded=(True, False, False, True),
                    container=False,
                    # width="100px",
                    # height="500px",
                )
                negative = gr.Textbox(
                    label="Enter your negative prompt",
                    show_label=False,
                    max_lines=10,
                    placeholder="Enter a negative prompt",
                    elem_id="negative-prompt-text-input",
                ).style(
                    border=(True, False, True, True),
                    rounded=(True, False, False, True),
                    container=False,
                    # width="100px",
                    # height="500px",
                )
                btn = gr.Button("Generate image", elem_id="generate-image-btn").style(
                    rounded=(False, True, True, False),
                    full_width=False,
                )
            with gr.Accordion("Advanced settings", open=False):
                samples = gr.Slider(label="Images", minimum=1, maximum=4, value=4, step=1)
                Width = gr.Slider(label="Width", minimum=256, maximum=2048, value=512, step=1)
                Height = gr.Slider(label="Height", minimum=256, maximum=2048, value=512, step=1)
                steps = gr.Slider(label="Steps", minimum=1, maximum=250, value=50, step=1)
                refiner_strength = gr.Slider(label="Refiner Strength (refiner not enabled)", minimum=0, maximum=0, value=0, step=0)
                guidance_scale = gr.Slider(
                    label="Guidance Scale", minimum=0, maximum=50, value=default_guidance_scale, step=0.1
                )
                seed = gr.Slider(
                    label="Seed",
                    minimum=-1,
                    maximum=2147483647,
                    step=1,
                    randomize=True,
                )
                scheduler_list = list(scheduler_mapping.keys())
                scheduler = gr.Dropdown(label="Scheduler", choices = scheduler_list, value = "EulerAncestralDiscreteScheduler")
            with gr.Accordion(label="License", open=False):
                gr.HTML(
                    """<div class="acknowledgments">
                        <p><h4>LICENSE</h4>
                        The SDXL 1.0 model is licensed with a <a href="https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/LICENSE.md" style="text-decoration: underline;" target="_blank">Stability AI CreativeML Open RAIL++-M</a> license. The License allows users to take advantage of the model in a wide range of settings (including free use and redistribution) as long as they respect the specific use case restrictions outlined, which correspond to model applications the licensor deems ill-suited for the model or are likely to cause harm. For the full list of restrictions please <a href="https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/LICENSE.md" style="text-decoration: underline;" target="_blank">read the license</a>.
                        <p><h4>Biases and content acknowledgment</h4>
                        Despite how impressive being able to turn text into image is, beware to the fact that this model may output content that reinforces or exacerbates societal biases, as well as realistic faces, pornography and violence. The model was trained on the <a href="https://laion.ai/blog/laion-5b/" style="text-decoration: underline;" target="_blank">LAION-5B dataset</a>, which scraped non-curated image-text-pairs from the internet (the exception being the removal of illegal content) and is meant for research purposes. You can read more in the <a href="https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0" style="text-decoration: underline;" target="_blank">model card</a></p>
                    </div>
                    """
                )
        with gr.Column(style={"width": "50%"}):
            gallery = gr.Gallery(
                label="Generated images", show_label=False, elem_id="gallery"
            ).style(grid=[2], height="auto")

            ex = gr.Examples(examples=examples, fn=infer, inputs=[text, negative, guidance_scale], outputs=[gallery], cache_examples=False)
            ex.dataset.headers = [""]
            negative.submit(infer, inputs=[text, negative, guidance_scale, samples, Width, Height, steps, refiner_strength, seed, scheduler], outputs=[gallery], postprocess=False)
            text.submit(infer, inputs=[text, negative, guidance_scale, samples, Width, Height, steps, refiner_strength, seed, scheduler], outputs=[gallery], postprocess=False)
            btn.click(infer, inputs=[text, negative, guidance_scale, samples, Width, Height, steps, refiner_strength, seed, scheduler], outputs=[gallery], postprocess=False)



#使用demo.queue()或demo.launch()启动交互式界面
block.queue() 

#将Gradio的界面demo挂载到FastAPI应用程序app中，并使用环境变量OPENI_SELF_URL中指定的路径。
app = gr.mount_gradio_app(app, block, path=os.getenv('OPENI_SELF_URL')) 
uvicorn.run(app, host='0.0.0.0', port=int(os.getenv('OPENI_SELF_PORT')))