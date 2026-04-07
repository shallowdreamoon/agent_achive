from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.agents.layout_agent import IPLayoutPlanningAgent
from backend.agents.litigation_agent import IPLitigationAnalysisAgent
from backend.agents.qa_agent import IPRiskQAAgent
from backend.core.config import get_settings
from backend.core.llm import LLMClient
from backend.data.vector_store import IPBenchStore
from backend.evaluation.benchmark import BenchmarkRunner
from backend.models.schemas import BenchmarkResponse, ConfigResponse, RunRequest, RunResponse
from backend.router.agent_router import AgentRouter
from backend.tools.evaluation_tool import EvaluationTool
from backend.tools.reasoning_tool import ReasoningTool
from backend.tools.search_tool import SearchTool

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

settings = get_settings()
llm_client = LLMClient(settings)
store = IPBenchStore(data_path=BASE_DIR / "data" / "ipbench_samples.json", llm_client=llm_client)
search_tool = SearchTool(store)
reasoning_tool = ReasoningTool(llm_client)
evaluation_tool = EvaluationTool()

router = AgentRouter(
    qa=IPRiskQAAgent(search_tool, reasoning_tool),
    layout=IPLayoutPlanningAgent(search_tool, reasoning_tool),
    litigation=IPLitigationAnalysisAgent(search_tool, reasoning_tool),
)
benchmark_runner = BenchmarkRunner(router=router, evaluation_tool=evaluation_tool, dataset_path=BASE_DIR / "evaluation" / "benchmark_dataset.json")

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origins] if settings.cors_origins != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/config", response_model=ConfigResponse)
def config():
    return ConfigResponse(
        mock_mode=settings.mock_mode,
        model=settings.openai_model,
        llm_available=llm_client.llm_available(),
    )


@app.post("/api/run", response_model=RunResponse)
def run_agent(payload: RunRequest):
    selected_agent, reason = router.select(payload.query, payload.agent_type)
    agent = router.dispatch(selected_agent)
    run = agent.run(query=payload.query, extra_params=payload.extra_params)
    return RunResponse(
        selected_agent=selected_agent,
        routing_reason="manual selection" if payload.agent_type else reason,
        structured_result=run["structured_result"],
        evidence=run["evidence"],
        raw_model_output=run["raw_model_output"],
        latency_ms=run["latency_ms"],
        mock_mode=True,
    )


@app.post("/api/benchmark/run", response_model=BenchmarkResponse)
def run_benchmark():
    return BenchmarkResponse.model_validate(benchmark_runner.run(PROJECT_ROOT / "outputs"))
