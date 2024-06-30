#!/usr/bin/env python3
#coding=utf-8

import subprocess
import gradio as gr
from PIL import Image
from io import BytesIO
import gpiozero

# 创建GPIO对象
led1 = gpiozero.LED(4)
led2 = gpiozero.LED(17)

def take_photo():
    try:
        # 设置GPIO 4和17为高电平
        led1.on()
        led2.on()

        # 尝试使用rpicam-still拍照
        try:
            process = subprocess.Popen(["rpicam-still", "-o", "-"], stdout=subprocess.PIPE)
        except FileNotFoundError:
            # 如果rpicam-still不存在，则使用libcamera-still
            process = subprocess.Popen(["libcamera-still", "-o", "-"], stdout=subprocess.PIPE)

        stdout, stderr = process.communicate()

        # 将图片数据转换为Pillow图像对象
        image = Image.open(BytesIO(stdout))
    finally:
        # 完成后恢复GPIO 4和17为低电平
        led1.off()
        led2.off()

    return image

# 创建Gradio界面
iface = gr.Interface(
    fn=take_photo,
    inputs=[],
    outputs=gr.Image(type="pil", label="Captured Photo"),
    title="Photo Capture",
    css="footer{display:none !important}",
    allow_flagging="never",
    clear_btn=None,
)
iface.launch(server_name="0.0.0.0")  # 启动Gradio应用
