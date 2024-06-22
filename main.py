from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image
import io
import subprocess
import base64
from gpiozero import LED

app = Flask(__name__)

# 设置GPIO
led1 = LED(4)
led2 = LED(17)

# 拍照函数
def take_photo():
    # 设置GPIO4和GPIO17为高电平
    led1.on()
    led2.on()
    
    # 使用libcamera-still命令行工具捕获图像
    process = subprocess.run(["libcamera-still", "-o", "-"], stdout=subprocess.PIPE)
    if process.returncode != 0:
        print("Failed to capture image")
        led1.off()
        led2.off()
        return None

    # 将捕获的图像转换为PIL图像
    img = Image.open(io.BytesIO(process.stdout))
    
    # 将PIL图像转换为字节流
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # 将字节流编码为base64字符串
    img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
    
    # 设置GPIO4和GPIO17为低电平
    led1.off()
    led2.off()
    
    return img_base64

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/take_photo', methods=['POST'])
def take_photo_route():
    photo_base64 = take_photo()
    return jsonify(photo_base64=photo_base64)

@app.route('/photo/<path:photo_base64>')
def get_photo(photo_base64):
    # 将base64字符串解码为字节流
    img_byte_arr = base64.b64decode(photo_base64)
    
    # 将字节流转换为PIL图像
    img = Image.open(io.BytesIO(img_byte_arr))
    
    # 将PIL图像保存到文件
    photo_path = 'static/latest_photo.jpg'
    img.save(photo_path)
    
    return send_file(photo_path)

if __name__ == '__main__':
    app.run(host='192.168.50.6', port=5000)
