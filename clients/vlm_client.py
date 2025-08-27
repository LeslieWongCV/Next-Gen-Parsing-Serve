# clients/vlm_client.py
import os
import base64
import json
from typing import Dict, Any

from openai import AsyncOpenAI
from config.settings import TIMEOUT
from dotenv import load_dotenv

load_dotenv()
print(os.environ["DASHSCOPE_API_KEY"])
# 初始化异步客户端（在模块加载时创建一次）

client = AsyncOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 默认模型（可从 settings 或传参配置）
DEFAULT_MODEL = "qwen-vl-max"  # 或 qwen-vl-plus


async def async_call_vlm(
    prompt: str,
    image_bytes: bytes,
    model: str = DEFAULT_MODEL,
    response_format: Dict[str, str] = None,
    temperature: float = 0.1
) -> str:
    """
    异步调用 Qwen-VL（通过 DashScope OpenAI 兼容接口）

    Args:
        prompt: 文本提示
        image_bytes: 图像原始字节
        model: 模型名称
        response_format: 如 {"type": "json_object"}，要求返回 JSON
        temperature: 生成温度

    Returns:
        模型返回的文本内容（字符串）
    """
    # 将图像转为 base64 编码
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    image_media_type = "image/jpeg"  # 可根据实际扩展判断

    # 构建 messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{image_media_type};base64,{base64_image}"
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ],
        }
    ]

    # 设置默认 response_format
    if response_format is None:
        response_format = {"type": "text"}  # 默认文本，usecase 可覆盖

    try:
        completion = await client.chat.completions.create(
            model=model,
            messages=messages,
            response_format=response_format,
            temperature=temperature,
            timeout=TIMEOUT,
        )

        content = completion.choices[0].message.content.strip()
        return content

    except Exception as e:
        raise RuntimeError(f"Error calling VLM API: {str(e)}") from e