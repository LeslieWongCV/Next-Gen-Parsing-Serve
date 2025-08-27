# usecases/image_caption.py
from .base import BaseUsecase
from processors.image_processor import resize_image, image_to_bytes
from processors.prompt_builder import get_prompt
from PIL import Image
import io
import base64

class ImageCaption(BaseUsecase):
    vlm_params = {
        "model": "qwen-vl-plus",  # 可用稍低成本模型
        "temperature": 0.2,
        "response_format": {"type": "text"}
    }

    async def preprocess(self, data):
        content = data["image"]
        image_bytes = base64.b64decode(content) if isinstance(content, str) else content
        image = Image.open(io.BytesIO(image_bytes))
        image = resize_image(image)
        final_bytes = image_to_bytes(image)

        return {
            "image_bytes": final_bytes
        }

    def build_prompt(self, proc_data):
        return get_prompt("image_caption")

    async def postprocess(self, raw_response, original_data):
        return {
            "usecase": "image_caption",
            "caption": raw_response.strip()
        }