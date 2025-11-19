from io import BytesIO
import random
from captcha.image import ImageCaptcha
import string
from typing import Tuple


def generate_numeric_captcha_text(length: int = 4) -> str:
    """生成指定长度的数字验证码"""
    return ''.join(random.choices(string.digits, k=length))


def generate_captcha() -> Tuple[BytesIO,str]:
    """生成随机验证码图片流，并返回图片流和验证码字符串"""
    image = ImageCaptcha(width=160, height=60, fonts=None)
    text = generate_numeric_captcha_text()
    captcha_data = image.generate_image(text)
    image_stream = BytesIO()
    captcha_data.save(image_stream,format='PNG')
    image_stream.seek(0)
    return image_stream,text

if __name__ == '__main__':
    img,text=generate_captcha()
    print(img)
    print(text)
