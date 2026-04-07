# Frontend Expected States（源码行为说明）

## 首页默认状态
- `agentType=auto`
- query 默认填充 QA 示例
- `result=null` / `benchmark=null`
- 不显示 AgentPanel / EvalPanel

## 运行中状态
- 点击“运行 Agent”后 `loadingRun=true`，按钮文案显示“运行中...”并禁用
- 点击“运行 Benchmark”后 `loadingBench=true`，按钮文案显示“评估中...”并禁用

## 成功返回状态
- `/api/run` 成功：渲染 selected_agent、routing_reason、latency_ms、structured_result、evidence
- `/api/benchmark/run` 成功：渲染 summary（overall/evidence/structured）+ per_agent_score 柱状 + case 列表

## 错误状态
- 任一请求失败：`setError(String(e))`，页面顶部显示红色错误条

## benchmark 展示状态
- `benchmark` 非空时显示 EvalPanel
- 指标读取字段：
  - `summary.average_overall_score`
  - `summary.evidence_hit_rate`
  - `summary.structured_output_validity`
  - `summary.per_agent_score`
