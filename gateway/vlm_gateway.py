# gateway/vlm_gateway.py
from ray import serve
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional


app = FastAPI(
    title="VLM Gateway API",
    description="Unified gateway for Document QA, Image Caption, Invoice Extraction",
    version="1.0.0"
)


# 🔹 定义请求模型
class DocumentQARequest(BaseModel):
    image: str  # base64 string
    question: str


class ImageCaptionRequest(BaseModel):
    image: str  # base64 string


class InvoiceExtractionRequest(BaseModel):
    image: str  # base64 string


@serve.deployment
@serve.ingress(app)
class VLMGateway:
    def __init__(self, doc_qa, image_caption, invoice_extract):
        self._doc_qa = doc_qa
        self._image_caption = image_caption
        self._invoice_extract = invoice_extract

    @app.get("/healthz")
    async def health(self):
        return {"status": "healthy"}

    @app.post("/document-qa", response_model=dict)
    async def document_qa(self, data: DocumentQARequest):  # ✅ 使用模型
        result = await self._doc_qa.remote(data.dict())
        return result

    @app.post("/image-caption", response_model=dict)
    async def image_caption(self, data: ImageCaptionRequest):  # ✅ 使用模型
        result = await self._image_caption.remote(data.dict())
        return result

    @app.post("/invoice-extraction", response_model=dict)
    async def invoice_extraction(self, data: InvoiceExtractionRequest):  # ✅ 使用模型
        result = await self._invoice_extract.remote(data.dict())
        return result