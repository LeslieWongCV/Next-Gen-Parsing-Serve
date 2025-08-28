# serve_app.py

from deployments.usecase_deployments import (
    DocumentQADeployment,
    ImageCaptionDeployment,
    InvoiceExtractionDeployment,
)
from gateway.vlm_gateway import VLMGateway

def create_app(args: dict):  # ✅ 必须加一个参数
    """
    args: 从 YAML 传入的参数
    """
    app = VLMGateway.bind(
        DocumentQADeployment.bind(),
        ImageCaptionDeployment.bind(),
        InvoiceExtractionDeployment.bind(),
    )
    return app
