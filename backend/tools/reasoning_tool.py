import json
from typing import Dict, List, Literal, Tuple, Type

from pydantic import BaseModel, Field

from backend.core.llm import LLMClient


class QASchema(BaseModel):
    question: str
    risk_type: str
    country_or_region: str
    analysis: str
    recommendations: List[str]
    evidence: List[str]


class LayoutSchema(BaseModel):
    technology_summary: str
    target_regions: List[str]
    filing_strategy: List[str]
    timeline_suggestion: List[str]
    risk_notes: List[str]
    evidence: List[str]


class LitigationSchema(BaseModel):
    case_summary: str
    potential_issues: List[str]
    litigation_risk: str
    suggested_actions: List[str]
    legal_path_notes: List[str]
    evidence: List[str]


class ReasoningTool:
    name = "reasoning_tool"

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def run(self, agent: Literal["qa", "layout", "litigation"], query: str, evidence: List[Dict], extra_params: Dict) -> Tuple[Dict, Dict]:
        schema, prompt = self._build_prompt(agent, query, evidence, extra_params)
        output = self.llm_client.chat_structured(system_prompt=prompt[0], user_prompt=prompt[1], schema_model=schema)
        return output, output

    def _build_prompt(self, agent: str, query: str, evidence: List[Dict], extra_params: Dict) -> Tuple[Type[BaseModel], Tuple[str, str]]:
        evidence_block = json.dumps(evidence, ensure_ascii=False, indent=2)
        base_system = (
            "You are an IP expert assistant. Use evidence only; if uncertain, say assumptions. "
            "Return strict JSON that matches schema."
        )
        if agent == "qa":
            user = (
                f"Task: IP risk Q&A\nQuestion: {query}\nExtra: {json.dumps(extra_params, ensure_ascii=False)}\n"
                f"Evidence:\n{evidence_block}"
            )
            return QASchema, (base_system, user)

        if agent == "layout":
            user = (
                "Task: IP layout planning. Provide filing steps and timeline.\n"
                f"Technology Input: {query}\nExtra: {json.dumps(extra_params, ensure_ascii=False)}\nEvidence:\n{evidence_block}"
            )
            return LayoutSchema, (base_system, user)

        user = (
            "Task: Litigation analysis. Focus on legal risk and possible response path.\n"
            f"Case Input: {query}\nExtra: {json.dumps(extra_params, ensure_ascii=False)}\nEvidence:\n{evidence_block}"
        )
        return LitigationSchema, (base_system, user)
