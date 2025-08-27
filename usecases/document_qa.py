# usecases/document_qa.py
from .base import BaseUsecase
from processors.image_processor import pdf_to_images, resize_image, correct_inversion, image_to_bytes, robust_base64_decode
from processors.prompt_builder import get_prompt
from PIL import Image
import io
import base64

class DocumentQA(BaseUsecase):
    # 问答不需要 JSON 输出
    vlm_params = {
        "model": "qwen-vl-max",
        "temperature": 0.1,
        "response_format": {"type": "text"}
    }

    async def preprocess(self, data):
        content = data["image"]  # 可能是 base64 字符串或 bytes
        question = data.get("question", "")

        # 使用健壮解码
        if isinstance(content, str):
            try:
                image_bytes = robust_base64_decode(content)
            except Exception as e:
                raise ValueError(f"Base64 decode failed: {str(e)}")
        else:
            image_bytes = content

        # PDF or Image
        content_type = data.get("content_type", "image/jpeg")
        if content_type == "application/pdf":
            images = pdf_to_images(image_bytes)
            image = images[0]
        else:
            image = Image.open(io.BytesIO(image_bytes))

        image = correct_inversion(image)
        image = resize_image(image)
        final_bytes = image_to_bytes(image)

        return {
            "image_bytes": final_bytes,
            "question": question
        }

    def build_prompt(self, proc_data):
        return get_prompt("document_qa", question=proc_data["question"])

    async def postprocess(self, raw_response, original_data):
        return {
            "usecase": "document_qa",
            "question": original_data["question"],
            "answer": raw_response
        }