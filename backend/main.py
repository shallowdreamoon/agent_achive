from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.agents.layout_agent import IPLayoutPlanningAgent
from backend.agents.litigation_agent import IPLitigationAnalysisAgent
from backend.agents.qa_agent import IPRiskQAAgent
from backend.data.vector_store import IPBenchStore
from backend.evaluation.benchmark import BenchmarkRunner
from backend.models.schemas import AgentRequest, AgentResponse, EvaluationResult
from backend.router.agent_router import AgentRouter
from backend.tools.evaluation_tool import EvaluationTool
from backend.tools.reasoning_tool import ReasoningTool
from backend.tools.search_tool import SearchTool

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

store = IPBenchStore(
    data_path=BASE_DIR / "data" / "ipbench_samples.json",
    persist_dir=PROJECT_ROOT / "vector_db",
)
search_tool = SearchTool(store)
reasoning_tool = ReasoningTool()
evaluation_tool = EvaluationTool()

router = AgentRouter(
    qa=IPRiskQAAgent(search_tool, reasoning_tool),
    layout=IPLayoutPlanningAgent(search_tool, reasoning_tool),
    litigation=IPLitigationAnalysisAgent(search_tool, reasoning_tool),
)
benchmark_runner = BenchmarkRunner(evaluation_tool)

app = FastAPI(title="IPBench-Based Intelligent Agents")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"ok": True, "agents": ["qa", "layout", "litigation"]}


@app.post("/api/agent", response_model=AgentResponse)
def run_agent(payload: AgentRequest):
    agent = router.dispatch(payload.agent)
    result = agent.run(payload.query, country=payload.country)
    return AgentResponse(agent=payload.agent, **result)


@app.get("/api/evaluate", response_model=EvaluationResult)
def evaluate():
    result = benchmark_runner.run(PROJECT_ROOT / "backend" / "evaluation" / "results.json")
    return EvaluationResult(**result)


@app.get("/api/demo-cases")
def demo_cases():
    return {
        "qa": [
            "我们在美国销售智能音箱，商标是否会侵权？",
            "进入印度远程医疗市场有哪些商标风险？",
            "阿联酋阿拉伯语音译商标冲突怎么判断？",
        ],
        "layout": [
            "电池管理算法要进入美国和加拿大，怎么布局专利？",
            "机器人控制系统18个月后进入欧洲，申请节奏建议？",
            "可穿戴设备外观想保护US/EU/JP，如何安排？",
        ],
        "litigation": [
            "收到美国NPE专利警告函，应诉路径是什么？",
            "德国被诉传感器专利侵权，如何降低禁令风险？",
            "法国海关扣押平行进口货物，如何应对？",
        ],
    }
