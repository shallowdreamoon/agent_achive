from typing import Any, Dict, List, Type

from pydantic import BaseModel

from backend.core.config import Settings


class LLMClient:
    def __init__(self, settings: Settings):
        self.settings = settings

    def llm_available(self) -> bool:
        return False

    def chat_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        schema_model: Type[BaseModel],
    ) -> Dict[str, Any]:
        _ = system_prompt
        _ = user_prompt
        return self._mock_response(schema_model)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        return [self._hash_embedding(text) for text in texts]

    @staticmethod
    def _mock_response(schema_model: Type[BaseModel]) -> Dict[str, Any]:
        data = {}
        for field_name, field in schema_model.model_fields.items():
            annotation = str(field.annotation)
            if "list" in annotation.lower():
                data[field_name] = ["mock-item"]
            elif "float" in annotation.lower():
                data[field_name] = 0.5
            else:
                data[field_name] = f"mock-{field_name}"
        return schema_model.model_validate(data).model_dump()

    @staticmethod
    def _hash_embedding(text: str, dim: int = 256) -> List[float]:
        vector = [0.0] * dim
        for token in text.lower().split():
            idx = hash(token) % dim
            vector[idx] += 1.0
        norm = sum(v * v for v in vector) ** 0.5 or 1.0
        return [v / norm for v in vector]
