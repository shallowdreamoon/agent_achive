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

    def dispatch(self, agent_name: str):
        if agent_name not in self.mapping:
            raise ValueError(f"Unknown agent: {agent_name}")
        return self.mapping[agent_name]
