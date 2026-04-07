import json
from pathlib import Path
from typing import Dict, List, Optional


class IPBenchStore:
    """IPBench vector retrieval with Chroma backend and lexical fallback."""

    def __init__(self, data_path: Path, persist_dir: Path):
        self.data_path = data_path
        self.persist_dir = persist_dir
        self.items: List[Dict] = json.loads(data_path.read_text(encoding="utf-8"))
        self._id_to_item = {x["id"]: x for x in self.items}
        self.use_chroma = False
        self.collection = None
        self._init_chroma()

    def _init_chroma(self) -> None:
        try:
            import chromadb

            self.persist_dir.mkdir(parents=True, exist_ok=True)
            client = chromadb.PersistentClient(path=str(self.persist_dir))
            self.collection = client.get_or_create_collection("ipbench")
            if self.collection.count() == 0:
                self.collection.add(
                    ids=[x["id"] for x in self.items],
                    documents=[" ".join([x["title"], x["content"], x["advice"], x["risk_type"], x["country"]]) for x in self.items],
                    metadatas=[{"task": x["task"], "country": x["country"], "risk_type": x["risk_type"]} for x in self.items],
                )
            self.use_chroma = True
        except Exception:
            self.use_chroma = False

    def _fallback_score(self, query: str, text: str) -> float:
        q_tokens = set(query.lower().split())
        t_tokens = set(text.lower().split())
        overlap = len(q_tokens & t_tokens)
        return overlap / (len(q_tokens) + 1e-9) if q_tokens else 0.0

    def semantic_search(self, query: str, k: int = 4, task_filter: Optional[str] = None) -> List[Dict]:
        if self.use_chroma and self.collection is not None:
            where = {"task": task_filter} if task_filter else None
            result = self.collection.query(query_texts=[query], n_results=k, where=where)
            ids = result.get("ids", [[]])[0]
            distances = result.get("distances", [[]])[0] if result.get("distances") else [0.0] * len(ids)
            payload = []
            for idx, item_id in enumerate(ids):
                base = self._id_to_item[item_id]
                payload.append(
                    {
                        "id": base["id"],
                        "title": base["title"],
                        "content": base["content"],
                        "score": round(max(0.0, 1.0 - float(distances[idx])), 4),
                        "country": base["country"],
                        "task": base["task"],
                        "risk_type": base["risk_type"],
                        "advice": base["advice"],
                    }
                )
            return payload

        scored = []
        for item in self.items:
            if task_filter and item["task"] != task_filter:
                continue
            text = " ".join([item["title"], item["content"], item["advice"], item["risk_type"], item["country"]])
            scored.append((self._fallback_score(query, text), item))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {
                "id": d["id"],
                "title": d["title"],
                "content": d["content"],
                "score": round(float(s), 4),
                "country": d["country"],
                "task": d["task"],
                "risk_type": d["risk_type"],
                "advice": d["advice"],
            }
            for s, d in scored[:k]
        ]
