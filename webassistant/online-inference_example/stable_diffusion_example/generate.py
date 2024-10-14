import gc
import os
from typing import Literal

from typing import Optional
from pydantic import BaseModel
from fastapi import UploadFile

import streamlit as st
import torch
import deepl
from diffusers import (
    DiffusionPipeline,
    StableDiffusionPipeline,
    StableDiffusionXLPipeline,
    StableDiffusion3Pipeline,
)


from diffusers import (
    DDPMScheduler,
    DDIMScheduler,
    PNDMScheduler,
    LMSDiscreteScheduler,
    EulerAncestralDiscreteScheduler,
    EulerDiscreteScheduler,
    DPMSolverMultistepScheduler,
)

# 定义调度器简写映射
scheduler_mapping = {
    "DDPMScheduler": DDPMScheduler,
    "DDIMScheduler": DDIMScheduler,
    "PNDMScheduler": PNDMScheduler,
    "LMSDiscreteScheduler": LMSDiscreteScheduler,
    "EulerAncestralDiscreteScheduler": EulerAncestralDiscreteScheduler,
    "EulerDiscreteScheduler": EulerDiscreteScheduler,
    "DPMSolverMultistepScheduler": DPMSolverMultistepScheduler,
}

MODEL_VERSIONS = Literal["1.5", "2.0", "2.1", "XL 1.0", "XL 1.0 refiner", "SDXL Turbo"]

class ImageRequest(BaseModel):
    prompt: str
    pipeline_name: str = "text2img"
    image_input: Optional[UploadFile] = None
    mask_input: Optional[UploadFile] = None
    negative_prompt: Optional[str] = None
    steps: int = 50
    width: int = 768
    height: int = 768
    guidance_scale: float = 7.5
    enable_attention_slicing: bool = False
    enable_cpu_offload: bool = False
    version: str = "XL 1.0"
    strength: float = 1.0
    seed:int = 1
    num_images_per_prompt:int = 1
    scheduler_name: str = "EulerDiscreteScheduler"

def get_scheduler(scheduler_type, model_id):
    scheduler_class = scheduler_mapping.get(scheduler_type, None)
    if scheduler_class:
        scheduler = scheduler_class.from_pretrained(model_id, subfolder="scheduler")
        return scheduler
    else:
        raise ValueError("Invalid scheduler type")

@st.cache_resource(max_entries=1)
def get_pipeline(
    model_id,
    scheduler_type,
    name,
    version: MODEL_VERSIONS = "XL 1.0",
    enable_cpu_offload=False,
) -> DiffusionPipeline:
    pipe = None

    if name == "text2img" and version in ("XL 1.0", "SDXL Turbo"):
        model_id = model_id
        pipe = StableDiffusionXLPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            use_safetensors=True,
            variant="fp16",
        )
    elif name in ["text2img", "img2img"] and version in ["3.0", "2.1"]:
        model_id = model_id
        pipe = StableDiffusion3Pipeline.from_pretrained(
            model_id,
            # text_encoder_3=None,
            # tokenizer_3=None,
            torch_dtype=torch.float16
        )

    if pipe is None:
        raise Exception(f"Could not find pipeline {name} and version {version}")

    if enable_cpu_offload:
        print("Enabling CPU offload for pipeline")
        # If we're reeeally strapped for memory, the sequential cpu offload can be used.
        # pipe.enable_sequential_cpu_offload()
        pipe.enable_model_cpu_offload()
    else:
        pipe = pipe.to("cuda") 
    return pipe

def generate(
    prompt,
    pipeline_name,
    model_id,
    pipe=None,
    image_input=None,
    mask_input=None,
    negative_prompt=None,
    steps=50,
    width=768,
    height=768,
    guidance_scale=7.5,
    enable_attention_slicing=False,
    enable_cpu_offload=False,
    version="2.1",
    strength=1.0,
    seed = 1,
    num_images_per_prompt = 2,
    scheduler_name = "EulerDiscreteScheduler",
):
    """Generates an image based on the given prompt and pipeline name"""
    negative_prompt = negative_prompt if negative_prompt else None
    p = st.progress(0)

    """load scheduler"""
    if version == "XL 1.0":
        scheduler_class = scheduler_mapping.get(scheduler_name, None)
        pipe.scheduler = scheduler_class.from_config(pipe.scheduler.config)

    def callback(pipe, step, timestep, callback_kwargs):
        p.progress(step / steps)
        return callback_kwargs

    # NOTE: This code is not being used
    refiner_version = None
    try:
        version, refiner_version = version.split(" + ")
    except:
        pass
    
    torch.cuda.empty_cache()

    if enable_attention_slicing:
        pipe.enable_attention_slicing()
    else:
        pipe.disable_attention_slicing()
    generator = torch.Generator("cuda").manual_seed(seed)
    kwargs = dict(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=steps,
        callback_on_step_end=callback,
        guidance_scale=guidance_scale,
        generator=generator,
        num_images_per_prompt= num_images_per_prompt,
    )

    # print("kwargs", kwargs)

    if pipeline_name == "inpaint" and image_input and mask_input:
        kwargs.update(image=image_input, mask_image=mask_input, strength=strength)
    elif pipeline_name == "text2img":
        kwargs.update(width=width, height=height, num_images_per_prompt = num_images_per_prompt)
    elif pipeline_name == "img2img" and image_input:
        kwargs.update(
            image=image_input,
        )
    else:
        raise Exception(
            f"Cannot generate image for pipeline {pipeline_name} and {prompt}"
        )

    high_noise_frac = 0.8

    # When a refiner is being used, we need to add the denoising_end/start parameters.
    # NOTE: This code is not being used
    if refiner_version:
        images = pipe(
            denoising_end=high_noise_frac, output_type="latent", **kwargs
        ).images
    else:
        images = pipe(**kwargs).images

    if refiner_version:
        images = images.detach().clone()
        pipe = None
        gc.collect()
        torch.cuda.empty_cache()
        refiner = get_pipeline(
            model_id,
            pipeline_name,
            version=refiner_version,
            enable_cpu_offload=enable_cpu_offload,
        )
        kwargs.pop("width", None)
        kwargs.pop("height", None)
        images = refiner(image=images, denoising_start=high_noise_frac, **kwargs).images
    return images

def pipe_init(
    model_id,
    schedulerMethod = "EulerAncestralDiscreteScheduler",
    name = "text2img",
    version="XL 1.0",
    enable_cpu_offload=False,
):
    pipe = get_pipeline(
        model_id, schedulerMethod, name, version=version, enable_cpu_offload=enable_cpu_offload
    )
    return pipe

def get_sd_model_dir(base_dir):
    import os
    # 获取指定目录下的所有文件夹
    folders = [folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder))]
    # 遍历文件夹
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        files = os.listdir(folder_path)
        if 'model_index.json' in files:
            print(f"文件夹 '{folder_path}' 非空且包含 model_index.json文件, 此路径为模型路径。")
            return folder_path
    return ""

def get_local_lora_id(base_dir,base_model_id):
    import os
    # 获取指定目录下的所有文件夹
    folders = [folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder))]
    # 遍历文件夹
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        if folder_path != base_model_id:
            files = os.listdir(folder_path)
            if any(file.endswith('.safetensors') for file in files):
                print(f"文件夹 '{folder_path}' 非空且包含 .safetensors 文件。")
                return folder_path
    return ""

def load_lora_weights(pipe, lora_model_id):
    pipe.load_lora_weights(lora_model_id)	    
    print(f"load lora..")	    
    return pipe    	    

def translation(prompt):
    if prompt is None:
        return None
    if prompt.encode('utf-8').isascii():  # 检查输入是否为英文
        return prompt
    else:
        translated_text = deepl.translate(source_language="ZH", target_language="EN", text=prompt)
        return translated_text