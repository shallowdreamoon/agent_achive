from typing import Dict, List, Optional

from backend.tools.reasoning_tool import ReasoningTool
from backend.tools.search_tool import SearchTool


class BaseIPAgent:
    task_filter: str

    def __init__(self, search_tool: SearchTool, reasoning_tool: ReasoningTool):
        self.search_tool = search_tool
        self.reasoning_tool = reasoning_tool

    def run(self, query: str, country: Optional[str] = None) -> Dict:
        search_query = f"{query} {country or ''}".strip()
        evidence = self.search_tool.run(search_query, task_filter=self.task_filter, k=4)
        structured = self.reasoning_tool.run(agent=self.task_filter, query=query, evidence=evidence)
        trace = [
            f"search_tool(task={self.task_filter})",
            "reasoning_tool(structured_output)",
        ]
        return {"answer": structured, "evidence": evidence, "trace": trace}
