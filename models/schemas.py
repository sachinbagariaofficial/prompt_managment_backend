from pydantic import BaseModel
from typing import Optional


class PromptFineTune(BaseModel):
    prompt: str
    temperature: float
    top_p: float
    top_k: int
    context: str
    tone: str
