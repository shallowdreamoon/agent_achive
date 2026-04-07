from typing import Dict, Optional, Tuple

from backend.agents.layout_agent import IPLayoutPlanningAgent
from backend.agents.litigation_agent import IPLitigationAnalysisAgent
from backend.agents.qa_agent import IPRiskQAAgent


class AgentRouter:
    def __init__(self, qa: IPRiskQAAgent, layout: IPLayoutPlanningAgent, litigation: IPLitigationAnalysisAgent):
        self.mapping = {
            "qa": qa,
            "layout": layout,
            "litigation": litigation,
        }

    def select(self, query: str, manual_agent: Optional[str]) -> Tuple[str, str]:
        if manual_agent:
            if manual_agent not in self.mapping:
                raise ValueError(f"Unknown agent type: {manual_agent}")
            return manual_agent, "manual agent_type specified by user"

        q = query.lower()
        if any(k in q for k in ["诉讼", "侵权", "警告函", "litigation", "lawsuit", "被诉"]):
            return "litigation", "query contains litigation/dispute intent"
        if any(k in q for k in ["布局", "申请", "pct", "planning", "filing", "timeline"]):
            return "layout", "query contains planning/filing intent"
        return "qa", "defaulted to risk Q&A based on generic question intent"

    def dispatch(self, selected_agent: str):
        return self.mapping[selected_agent]
