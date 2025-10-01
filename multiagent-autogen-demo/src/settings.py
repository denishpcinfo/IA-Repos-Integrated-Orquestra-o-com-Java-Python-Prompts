from pydantic import BaseModel
import os
class Settings(BaseModel):
    max_rounds: int = int(os.getenv("MAX_ROUNDS", 6))
    http_tool_url: str = os.getenv("HTTP_TOOL_URL", "https://httpbin.org/post")
    prompt_catalog_dir: str = os.getenv("PROMPT_CATALOG_DIR", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "prompt-engineering-catalog")))
settings = Settings()
