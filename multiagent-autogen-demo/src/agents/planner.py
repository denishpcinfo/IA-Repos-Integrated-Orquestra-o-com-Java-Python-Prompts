from typing import Dict, Optional
from ..prompts.loader import load_prompt, PromptNotFound
class Planner:
    def plan(self, user_goal: str, template_key: Optional[str] = None) -> Dict:
        prompt_template = None
        if template_key:
            try:
                prompt_template = load_prompt(template_key)
            except PromptNotFound as e:
                prompt_template = f"[WARN] {e}"
        return {"goal": user_goal, "prompt_template": prompt_template, "steps": ["Validar política", "Executar ação em API mock", "Auditar decisão"]}
