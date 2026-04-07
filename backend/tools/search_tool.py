from typing import Dict, List, Optional

from backend.data.vector_store import IPBenchStore


class SearchTool:
    name = "search_tool"

    def __init__(self, store: IPBenchStore):
        self.store = store

    def run(self, query: str, task_filter: Optional[str], k: int) -> List[Dict]:
        return self.store.semantic_search(query=query, task_filter=task_filter, k=k)
