# processors/prompt_builder.py
import yaml
from pathlib import Path

PROMPT_DIR = Path(__file__).parent.parent / "config" / "prompts.yaml"

with open(PROMPT_DIR, 'r', encoding='utf-8') as f:
    PROMPTS = yaml.safe_load(f)

def get_prompt(template_name: str, **kwargs) -> str:
    if template_name not in PROMPTS:
        raise ValueError(f"Prompt template '{template_name}' not found")
    prompt = PROMPTS[template_name]
    return prompt.format(**kwargs)