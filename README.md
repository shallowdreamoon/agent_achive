# 企业出海知识产权风险多智能体系统（Agent Achive）

一个可运行、可展示、可部署、可评估的多智能体 Demo，覆盖：
- **IP Risk QA Agent**（风险问答）
- **IP Layout Planning Agent**（专利布局规划）
- **IP Litigation Analysis Agent**（诉讼分析）

## 核心能力

- 自动/手动路由（返回 `selected_agent` 与 `routing_reason`）
- 检索增强执行链：`query -> router -> retrieval -> tool use -> llm reasoning -> structured response`
- OpenAI 兼容 LLM 调用（支持 `OPENAI_BASE_URL`）
- Embedding 检索 + 本地哈希 embedding 回退（统一接口）
- 真实 benchmark pipeline（逐 case 调 agent + 自动评分）
- React + Tailwind 前端，支持结果、证据、benchmark 图表展示

## 架构图

见 [architecture.md](./architecture.md)（含系统图、Agent workflow、Benchmark workflow）。

## 目录结构

```text
.
├── backend/
│   ├── core/                 # config + llm client
│   ├── agents/               # 三类 agent
│   ├── tools/                # search/reasoning/evaluation tools
│   ├── data/                 # ipbench samples
│   ├── router/               # auto/manual router
│   ├── evaluation/           # benchmark runner + dataset
│   └── main.py               # FastAPI 入口
├── frontend/                 # React + Vite + Tailwind
├── data/ipbench_demo.json    # 对外 demo 数据副本
├── outputs/                  # benchmark 输出
├── docker/
├── scripts/generate_artifacts.py
├── README.md
└── architecture.md
```

## 环境变量

后端（建议默认 mock 演示；可切换 real LLM）：

```bash
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
MOCK_MODE=true
ENABLE_REMOTE_EMBEDDING=false
DEFAULT_TOP_K=4
```

> `MOCK_MODE=true` 时将强制使用 mock 输出，便于离线演示；`MOCK_MODE=false` 时尝试调用 OpenAI 兼容接口。

## 本地启动

### 1) Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 2) Frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

访问：
- API: `http://localhost:8000/docs`
- UI: `http://localhost:5173`

## Docker 启动

```bash
docker compose up --build
```

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`

## API 说明

### `POST /api/run`
输入：
```json
{
  "query": "收到美国NPE专利警告函，应诉路径是什么？",
  "agent_type": "litigation",
  "extra_params": {"country": "US", "top_k": 4}
}
```
输出字段包含：
- `selected_agent`
- `routing_reason`
- `structured_result`
- `evidence`
- `raw_model_output`
- `latency_ms`
- `mock_mode`
- `model_name`

### `POST /api/benchmark/run`
运行完整 benchmark，返回：
- `summary`
- `detailed_results`

并写入：
- `outputs/benchmark_results.json`
- `outputs/benchmark_summary.json`

### `GET /api/health`
健康检查。

### `GET /api/config`
返回运行模式、模型名、mock 状态、可用 agents。

## Benchmark 数据与指标

- 数据集：`backend/evaluation/benchmark_dataset.json`（20 条，覆盖 3 类任务）
- 指标：
  - `task_coverage`
  - `evidence_hit_rate`
  - `structured_output_validity`
  - `keyword_match_score`
  - `average_overall_score`

## 前端页面说明

- 首页：Agent 选择、输入区、参数区、运行按钮
- 输出区：路由信息卡、结构化 JSON 卡、evidence 明细（可展开）
- Benchmark 面板：运行按钮、指标卡、柱状图、case 结果表

## Artifact 与截图占位

生成命令：

```bash
python scripts/generate_artifacts.py
```

会生成/更新：
- `docs/ui-placeholder.svg`
- `docs/benchmark-chart.svg`（依赖 outputs summary）

## Mock mode vs Real LLM mode

- **Real LLM mode（默认）**：调用 OpenAI 兼容接口进行结构化推理与 embedding
- **Mock mode**：仅在 `MOCK_MODE=true` 显式启用时强制 mock；适合离线展示

## 示例输出（节选）

```json
{
  "selected_agent": "qa",
  "routing_reason": "defaulted to risk Q&A based on generic question intent",
  "structured_result": {
    "question": "...",
    "risk_type": "Trademark",
    "country_or_region": "US",
    "analysis": "...",
    "recommendations": ["..."],
    "evidence": ["IPB-001"]
  }
}
```


## 一键交付验证

```bash
python scripts/verify_delivery.py
```

该脚本会自动调用：
- `GET /api/health`
- `GET /api/config`
- `POST /api/run`（`agent_type=qa`）

并写入 `outputs/`：
- `health_check.json`
- `config_check.json`
- `run_qa.json`

补充交付检查文件：
- `frontend_checklist.md`
- `api_samples.md`
- `docker_verification.md`
