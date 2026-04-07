# IPBench-Based Intelligent Agents for Overseas IP Risk Analysis

一个可交付的“企业出海知识产权风险智能体系统”，覆盖问答、布局规划、诉讼分析三类任务，基于 IPBench 示例数据构建检索增强与评估闭环。

## 1. 项目简介（用于汇报）

- **三智能体**：
  - IP Risk QA Agent（出海风险问答）
  - IP Layout Planning Agent（海外专利布局）
  - IP Litigation Analysis Agent（侵权诉讼分析）
- **数据层**：内置 20 条 IPBench 风格样本，支持 semantic search + task filtering。
- **调度层**：Router 负责 agent 路由，Tool 层统一 search/reasoning/evaluation 调用。
- **评估层**：输出 accuracy / reasoning score / task coverage（JSON + 图表）。
- **展示层**：React + Tailwind Web UI（非 CLI）。

## 2. 系统架构图

详见 [architecture.md](./architecture.md)，其中含 Mermaid 自动生成图。

## 3. 安装方式

### 本地开发

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd frontend && npm install && cd ..
```

## 4. 运行方式

### 方式 A：本地启动

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
# 新开终端
cd frontend && npm run dev -- --host 0.0.0.0 --port 5173
```

访问：
- 后端 API: http://localhost:8000/docs
- 前端 UI: http://localhost:5173

### 方式 B：Docker 一键启动

```bash
docker compose up --build
```

## 5. 示例截图（占位）

- UI 占位图：`docs/ui-placeholder.svg`（可替换为真实运行截图）
- Benchmark 图：`backend/evaluation/benchmark.svg`

## 6. Benchmark 结果说明

执行：
```bash
python -m backend.evaluation.run_eval
python scripts/generate_artifacts.py
```

输出：
- 结果 JSON：`backend/evaluation/results.json`
- 指标图：`backend/evaluation/benchmark.svg`

指标解释：
- **accuracy**：是否给出带证据的有效回答比例
- **reasoning score**：结构化推理完整度评分
- **task coverage**：三类任务覆盖度

## 7. 项目结构

```text
project_root/
├── backend/
│   ├── main.py
│   ├── agents/
│   ├── tools/
│   ├── data/
│   ├── evaluation/
│   └── router/
├── frontend/
│   ├── src/
│   └── components/
├── vector_db/
├── scripts/
├── docker/
├── README.md
└── architecture.md
```
