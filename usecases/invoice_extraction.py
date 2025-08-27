# usecases/invoice_extraction.py
from .base import BaseUsecase
from processors.image_processor import resize_image, correct_inversion, image_to_bytes
from processors.prompt_builder import get_prompt
from processors.response_parser import parse_json_response
from PIL import Image
import io
import base64

class InvoiceExtraction(BaseUsecase):
    # 明确要求返回 JSON
    vlm_params = {
        "model": "qwen-vl-max",
        "temperature": 0.1,
        "response_format": {"type": "json_object"}
    }

    async def preprocess(self, data):
        content = data["image"]
        image_bytes = base64.b64decode(content) if isinstance(content, str) else content
        image = Image.open(io.BytesIO(image_bytes))

        image = correct_inversion(image)
        image = resize_image(image)
        final_bytes = image_to_bytes(image)

        return {
            "image_bytes": final_bytes
        }

    def build_prompt(self, proc_data):
        return get_prompt("invoice_extraction")

    async def postprocess(self, raw_response, original_data):
        try:
            parsed = json.loads(raw_response)
        except json.JSONDecodeError:
            parsed = {"error": "Failed to parse JSON", "raw": raw_response}

        return {
            "usecase": "invoice_extraction",
            "extracted": parsed,
            "raw_response": raw_response
        }