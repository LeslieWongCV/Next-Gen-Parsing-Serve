# deployments/usecase_deployments.py
from ray import serve
from usecases import DocumentQA, InvoiceExtraction, ImageCaption


# ✅ 只保留 @serve.deployment()，不带参数
@serve.deployment
class DocumentQADeployment:
    def __init__(self):
        self.usecase = DocumentQA()

    async def __call__(self, data):
        return await self.usecase.execute(data)


@serve.deployment
class ImageCaptionDeployment:
    def __init__(self):
        self.usecase = ImageCaption()

    async def __call__(self, data):
        return await self.usecase.execute(data)


@serve.deployment
class InvoiceExtractionDeployment:
    def __init__(self):
        self.usecase = InvoiceExtraction()

    async def __call__(self, data):
        return await self.usecase.execute(data)