from pathlib import Path
from ..settings import settings
PROMPTS = {"policy_summary": "prompts/01_summarize_bank_policy.after.md", "contract_draft": "prompts/02_generate_contract.after.md"}
class PromptNotFound(Exception):
    pass

def load_prompt(key: str) -> str:
    rel = PROMPTS.get(key)
    if not rel:
        raise PromptNotFound(f"Prompt key '{key}' não mapeado.")
    base = Path(settings.prompt_catalog_dir)
    path = base / rel
    if not path.exists():
        raise PromptNotFound(f"Arquivo de prompt não encontrado: {path}")
    return path.read_text(encoding="utf-8")
