from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel


class BaseDigestor(BaseModel, ABC):
    llm_client: Any | None
    llm_kwargs: dict | None = {"model": "gpt-4o"}

    _template: str = r"""
    <SYS>{{task_desc_str}}</SYS>
    {# output format #}
    {% if output_format_str %}
    {{output_format_str}}
    {% endif %}
    User: {{input_str}}
    You:"""

    @abstractmethod
    def run(self, text: str) -> str: ...
