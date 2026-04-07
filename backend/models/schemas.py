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


class BenchmarkCase(BaseModel):
    id: str
    task_type: AgentType
    input: Dict[str, Any]
    reference: Dict[str, Any]
    expected_keywords: List[str]


class CaseScore(BaseModel):
    id: str
    agent: AgentType
    overall_score: float
    evidence_hit: float
    keyword_match: float
    structured_valid: float
    details: Dict[str, Any]


class BenchmarkSummary(BaseModel):
    task_coverage: float
    evidence_hit_rate: float
    structured_output_validity: float
    keyword_match_score: float
    average_overall_score: float
    per_agent_score: Dict[str, float]


class BenchmarkResponse(BaseModel):
    summary: BenchmarkSummary
    detailed_results: List[CaseScore]


class ConfigResponse(BaseModel):
    mock_mode: bool
    model_name: str
    embedding_model: str
    available_agents: List[AgentType]
    default_top_k: int
