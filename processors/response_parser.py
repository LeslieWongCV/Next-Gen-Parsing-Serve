# processors/response_parser.py
import json
import re

def parse_json_response(text: str) -> dict:
    try:
        # 提取第一个 { ... } 块
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            cleaned = match.group(0)
            return json.loads(cleaned)
    except Exception:
        pass
    return {"raw": text, "parsed": False}