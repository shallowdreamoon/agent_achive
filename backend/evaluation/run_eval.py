from pathlib import Path

from backend.agents.layout_agent import IPLayoutPlanningAgent
from backend.agents.litigation_agent import IPLitigationAnalysisAgent
from backend.agents.qa_agent import IPRiskQAAgent
from backend.core.config import get_settings
from backend.core.llm import LLMClient
from backend.data.vector_store import IPBenchStore
from backend.evaluation.benchmark import BenchmarkRunner
from backend.router.agent_router import AgentRouter
from backend.tools.evaluation_tool import EvaluationTool
from backend.tools.reasoning_tool import ReasoningTool
from backend.tools.search_tool import SearchTool


if __name__ == "__main__":
    settings = get_settings()
    llm_client = LLMClient(settings)
    store = IPBenchStore(data_path=Path("backend/data/ipbench_samples.json"), llm_client=llm_client)
    search = SearchTool(store)
    reasoning = ReasoningTool(llm_client)
    router = AgentRouter(
        qa=IPRiskQAAgent(search, reasoning),
        layout=IPLayoutPlanningAgent(search, reasoning),
        litigation=IPLitigationAnalysisAgent(search, reasoning),
    )
    runner = BenchmarkRunner(router=router, evaluation_tool=EvaluationTool(), dataset_path=Path("backend/evaluation/benchmark_dataset.json"))
    result = runner.run(Path("outputs"))
    print(result["summary"])
