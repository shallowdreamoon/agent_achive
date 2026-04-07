import time
from typing import Dict, Literal

from backend.tools.reasoning_tool import ReasoningTool
from backend.tools.search_tool import SearchTool


class BaseIPAgent:
    task_filter: Literal["qa", "layout", "litigation"]

    def __init__(self, search_tool: SearchTool, reasoning_tool: ReasoningTool):
        self.search_tool = search_tool
        self.reasoning_tool = reasoning_tool

    def run(self, query: str, extra_params: Dict) -> Dict:
        start = time.time()
        top_k = int(extra_params.get("top_k", 4))
        country = extra_params.get("country", "")
        search_query = f"{query} {country}".strip()
        evidence = self.search_tool.run(query=search_query, task_filter=self.task_filter, k=top_k)
        structured_result, raw = self.reasoning_tool.run(
            agent=self.task_filter,
            query=query,
            evidence=evidence,
            extra_params=extra_params,
        )
        latency_ms = int((time.time() - start) * 1000)
        return {
            "structured_result": structured_result,
            "raw_model_output": raw,
            "evidence": evidence,
            "latency_ms": latency_ms,
        }
