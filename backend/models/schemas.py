from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


AgentType = Literal["qa", "layout", "litigation"]


class RunRequest(BaseModel):
    query: str = Field(min_length=3)
    agent_type: Optional[AgentType] = None
    extra_params: Dict[str, Any] = Field(default_factory=dict)


class EvidenceItem(BaseModel):
    id: str
    task: str
    country: str
    title: str
    snippet: str
    score: float


class RunResponse(BaseModel):
    selected_agent: AgentType
    routing_reason: str
    structured_result: Dict[str, Any]
    evidence: List[EvidenceItem]
    raw_model_output: Optional[Dict[str, Any]] = None
    latency_ms: int
    mock_mode: bool


class BenchmarkCase(BaseModel):
    id: str
    task_type: AgentType
    input: Dict[str, Any]
    reference: Dict[str, Any]
    expected_keywords: List[str]


class BenchmarkSummary(BaseModel):
    average_score: float
    task_coverage: float
    evidence_hit_rate: float
    structured_output_validity: float


class BenchmarkResponse(BaseModel):
    summary: BenchmarkSummary
    details: List[Dict[str, Any]]


class ConfigResponse(BaseModel):
    mock_mode: bool
    model: str
    llm_available: bool
    available_agents: List[AgentType]
