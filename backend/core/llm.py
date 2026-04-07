from typing import Any, Dict, List, Type

from pydantic import BaseModel

from backend.core.config import Settings


class LLMClient:
    def __init__(self, settings: Settings):
        self.settings = settings

    def llm_available(self) -> bool:
        return bool(self.settings.openai_api_key)

    def chat_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        schema_model: Type[BaseModel],
    ) -> Dict[str, Any]:
        if self.settings.mock_mode:
            return self._mock_response(schema_model)

        if not self.llm_available():
            raise RuntimeError("Real LLM mode requires OPENAI_API_KEY, but key is missing.")

        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.settings.openai_api_key, base_url=self.settings.openai_base_url)
            completion = client.chat.completions.create(
                model=self.settings.openai_model,
                response_format={"type": "json_object"},
                temperature=0.2,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                timeout=self.settings.llm_timeout_seconds,
            )
            content = completion.choices[0].message.content or "{}"
            return schema_model.model_validate_json(content).model_dump()
        except Exception as exc:
            raise RuntimeError(f"Real LLM call failed: {exc}") from exc

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if self.settings.mock_mode or not self.settings.enable_remote_embedding:
            return [self._hash_embedding(text) for text in texts]

        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.settings.openai_api_key, base_url=self.settings.openai_base_url)
            result = client.embeddings.create(model=self.settings.embedding_model, input=texts)
            return [item.embedding for item in result.data]
        except Exception:
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
