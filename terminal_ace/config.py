import os
from dataclasses import dataclass

@dataclass
class Config:
    model_name: str = os.getenv("MODEL_NAME", "qwen2.5-coder-7b")
    sandbox_image: str = "terminal-ace-sandbox:latest"
    max_steps: int = 10
    api_url: str = os.getenv("API_URL", "http://localhost:8000/v1")