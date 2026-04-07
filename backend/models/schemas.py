from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    agent: str = Field(description="qa | layout | litigation")
    query: str
    country: Optional[str] = None
    task_filter: Optional[str] = None
    use_llm: bool = True


class Evidence(BaseModel):
    id: str
    title: str
    content: str
    score: float
    country: str
    task: str


class AgentResponse(BaseModel):
    agent: str
    answer: Dict[str, Any]
    evidence: List[Evidence]
    trace: List[str]


class EvaluationResult(BaseModel):
    accuracy: float
    reasoning_score: float
    task_coverage: float
    per_agent: Dict[str, Dict[str, float]]
