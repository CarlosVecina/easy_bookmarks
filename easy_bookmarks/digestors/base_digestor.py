from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel


class BaseDigestor(BaseModel, ABC):
    model_client: Any | None
    model_kwargs: dict | None = {"model": "gpt-4o"}

    _template: str = r"""
    <SYS>{{task_desc_str}}</SYS>
    User: {{input_str}}
    You:"""

    @abstractmethod
    def run(self, text: str) -> str: ...
