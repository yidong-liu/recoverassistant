'''只选一个sd xl的模型'''
from fastapi import FastAPI
from PIL import Image
from io import BytesIO
from datetime import datetime
from generate import ImageRequest, generate, pipe_init, get_sd_model_dir, translation
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

#初始化pipe
pipe = pipe_init(base_model_id, "EulerAncestralDiscreteScheduler", "text2img", "XL 1.0", False)

base_url = os.getenv('OPENI_SELF_URL')


@app.post(os.path.join(base_url,"text2image"))
async def generate_image(image_request: ImageRequest):

    image_input = None
    mask_input = None

    if image_request.image_input:
        image_input = Image.open(BytesIO(await image_request.image_input.read())).convert("RGB")

    if image_request.mask_input:
        mask_input = Image.open(BytesIO(await image_request.mask_input.read())).convert("L")

    generated_images = generate(
        translation(image_request.prompt),
        image_request.pipeline_name,
        model_id = base_model_id,
        pipe=pipe,
        image_input=image_input,
        mask_input=mask_input,
        negative_prompt=translation(image_request.negative_prompt),
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
        generated_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        image_base64_list.append(img_str)
        
    return {"image_base64_list": image_base64_list}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('OPENI_SELF_PORT')))