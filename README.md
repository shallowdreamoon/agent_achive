# Agent Achive Demo (Mock Version)

这是一个**今晚可演示的最小可运行 Demo**，用于展示多智能体流程（qa / layout / litigation）。

## 当前版本定位

- 当前版本是 **demo/mock version**。
- 已实现前后端联调和多 agent 演示流程。
- 尚未接入真实 LLM（统一 mock_mode=true）。
- 可作为汇报展示原型。

## 已实现能力

- 后端接口：
  - `GET /api/health`
  - `GET /api/config`
  - `POST /api/run`
  - `POST /api/benchmark/run`
- 前端页面：
  - agent 下拉框、query 输入框、run/benchmark 按钮
  - selected_agent、routing_reason、structured_result、evidence 展示
  - benchmark summary 展示

## 启动方式

### 后端

```bash
pip install -r requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## 一键验收脚本

```bash
python scripts/verify_delivery.py
```

脚本会调用接口并生成：

- `outputs/health_check.json`
- `outputs/config_check.json`
- `outputs/run_qa.json`
- `outputs/benchmark_summary.json`
