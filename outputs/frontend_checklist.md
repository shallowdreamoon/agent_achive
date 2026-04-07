# Frontend Delivery Checklist (2026-04-07 UTC)

## 1) 启动命令
- `cd frontend && npm install`
- `npm run dev -- --host 0.0.0.0 --port 5173`

## 2) 访问地址
- 本地开发地址：`http://localhost:5173`

## 3) 页面模块（基于源码核对）
- 头部说明区（系统标题+能力描述）
- 左侧控制面板：agent 选择、query 输入、country、top_k、运行按钮
- 右侧结果区：
  - `AgentPanel`：selected_agent / routing_reason / latency / structured_result / evidence
  - `EvalPanel`：benchmark summary 指标卡、per_agent_score 柱状、case 表格

## 4) 与后端联调状态
- 代码层面：已接入 `fetch(${API}/api/run)` 与 `fetch(${API}/api/benchmark/run)`。
- 本次环境实际联调：**失败**（npm registry 403，无法完成 `npm install`，因此无法启动前端进程）。

## 5) 功能可用性逐项结论（源码级核对 + 本环境实跑）
- agent 选择：**已实现（源码）**
- 输入提交：**已实现（源码）**
- evidence 展示：**已实现（源码）**
- routing_reason 展示：**已实现（源码）**
- benchmark 展示：**已实现（源码）**
- 错误提示：**已实现（源码）**（`error` alert）
- loading 状态：**已实现（源码）**（按钮文案“运行中.../评估中...”）

> 说明：以上“已实现”指源码功能存在；由于依赖下载被策略拦截，本次无法给出浏览器实机截图。
