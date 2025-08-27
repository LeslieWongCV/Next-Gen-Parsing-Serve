# processors/image_processor.py
from PIL import Image
import fitz  # PyMuPDF
import io
import numpy as np
import base64
import re

def pdf_to_images(pdf_bytes: bytes, dpi=96) -> list[Image.Image]:
    doc = fitz.open("pdf", pdf_bytes)
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        images.append(img)
    return images

def resize_image(image: Image.Image, max_size: int = 1024) -> Image.Image:
    w, h = image.size
    if w > max_size or h > max_size:
        scale = max_size / max(w, h)
        new_size = (int(w * scale), int(h * scale))
        return image.resize(new_size, Image.Resampling.LANCZOS)
    return image

def detect_inversion(image: Image.Image) -> bool:
    # 简单判断：左上角 10x10 区域是否偏暗（假设文字是深色）
    small = image.convert("L").resize((10, 10))
    pixels = np.array(small)
    avg = pixels.mean()
    return avg < 128  # 暗图可能是反色

def correct_inversion(image: Image.Image) -> Image.Image:
    if detect_inversion(image):
        return Image.eval(image, lambda x: 255 - x)
    return image

def image_to_bytes(image: Image.Image, format="JPEG") -> bytes:
    buf = io.BytesIO()
    image.convert("RGB").save(buf, format=format, quality=95)
    return buf.getvalue()


def robust_base64_decode(data: str) -> bytes:
    """
    健壮地解码 base64 字符串，支持：
    - 去除 data:image 前缀
    - 去除空白字符
    - 补齐 padding
    """
    if not isinstance(data, str):
        raise ValueError("Input must be a string")

    # 1. 去除 data:image/...;base64, 前缀
    data = re.sub(r"^data:image/[^;]+;base64,", "", data)

    # 2. 去除空白字符（换行、空格、制表符）
    data = re.sub(r"\s", "", data)

    # 3. 补齐 padding（Base64 必须是 4 的倍数）
    missing_padding = len(data) % 4
    if missing_padding:
        data += "=" * (4 - missing_padding)

    # 4. 解码
    try:
        return base64.b64decode(data)
    except Exception as e:
        raise ValueError(f"Invalid base64 string: {str(e)}")