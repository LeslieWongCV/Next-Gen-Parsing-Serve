# main.py
from ray import serve
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any


app = FastAPI()

# 导入 usecases
from usecases import DocumentQA, InvoiceExtraction, ImageCaption

@serve.deployment(
    num_replicas=2,
    ray_actor_options={"num_cpus": 1}
)
@serve.ingress(app)
class VLMGateway:
    def __init__(self):
        self.usecases = {
            "document_qa": DocumentQA(),
            "invoice_extraction": InvoiceExtraction(),
            "image_caption": ImageCaption(),
        }

    @app.post("/v1/run")
    async def run(self, request: Dict[Any, Any]):
        usecase = request.get("usecase")
        data = request.get("data")

        if not usecase or not data:
            raise HTTPException(400, "Missing 'usecase' or 'data'")

        if usecase not in self.usecases:
            raise HTTPException(400, f"Unknown usecase: {usecase}")

        executor = self.usecases[usecase]
        result = await executor.execute(data)
        return {"success": True, "result": result}

# 启动命令：serve run main:VLMGateway
app = VLMGateway.bind()