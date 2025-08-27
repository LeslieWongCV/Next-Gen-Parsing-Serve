# usecases/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseUsecase(ABC):
    # 子类可覆盖此字段，用于传给 async_call_vlm
    vlm_params = {
        "model": "qwen-vl-max",
        "temperature": 0.1,
        "response_format": {"type": "text"}  # 默认文本
    }

    @abstractmethod
    async def preprocess(self, data: Dict) -> Dict:
        pass

    @abstractmethod
    def build_prompt(self, processed_data: Dict) -> str:
        pass

    @abstractmethod
    async def postprocess(self, raw_response: str, original_data: Dict) -> Dict:
        pass

    async def execute(self, data: Dict) -> Dict:
        try:
            proc_data = await self.preprocess(data)
            prompt = self.build_prompt(proc_data)

            # 获取 usecase 自定义参数
            extra_args = getattr(self, "vlm_params", {})

            # 调用 VLM
            from clients.vlm_client import async_call_vlm
            raw_response = await async_call_vlm(prompt=prompt, image_bytes=proc_data["image_bytes"], **extra_args)

            # 后处理
            result = await self.postprocess(raw_response, data)
            result["success"] = True
            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }