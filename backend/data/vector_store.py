import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from backend.core.llm import LLMClient


@dataclass
class SearchDocument:
    id: str
    task: str
    country: str
    title: str
    content: str
    advice: str
    risk_type: str


class IPBenchStore:
    def __init__(self, data_path: Path, llm_client: LLMClient):
        self.data_path = data_path
        self.llm_client = llm_client
        self.docs = self._load_data()
        self.index_vectors = self.llm_client.embed_texts([self._to_index_text(d) for d in self.docs])

    def _load_data(self) -> List[SearchDocument]:
        payload = json.loads(self.data_path.read_text(encoding="utf-8"))
        return [SearchDocument(**item) for item in payload]

    @staticmethod
    def _normalize(text: str) -> str:
        return " ".join(text.lower().strip().split())

    def _to_index_text(self, doc: SearchDocument) -> str:
        merged = f"{doc.title}\n{doc.content}\n{doc.advice}\n{doc.risk_type}\n{doc.country}"
        return self._normalize(merged)

    @staticmethod
    def _cosine_similarity(a: List[float], b: List[float]) -> float:
        return sum(x * y for x, y in zip(a, b))

    def semantic_search(self, query: str, k: int = 4, task_filter: Optional[str] = None) -> List[Dict]:
        qv = self.llm_client.embed_texts([self._normalize(query)])[0]
        scored = []
        for i, doc in enumerate(self.docs):
            if task_filter and doc.task != task_filter:
                continue
            score = self._cosine_similarity(qv, self.index_vectors[i])
            scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)

        top_items = []
        for score, doc in scored[:k]:
            top_items.append(
                {
                    "id": doc.id,
                    "task": doc.task,
                    "country": doc.country,
                    "title": doc.title,
                    "snippet": doc.content,
                    "advice": doc.advice,
                    "risk_type": doc.risk_type,
                    "score": round(float(score), 4),
                }
            )
        return top_items
