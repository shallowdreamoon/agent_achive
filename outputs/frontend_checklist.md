# Frontend Checklist (2026-04-07 UTC)

## 前端启动命令
- `cd frontend && npm install`
- `npm run dev -- --host 127.0.0.1 --port 5173`

## 前端访问地址
- `http://127.0.0.1:5173/`

## 页面模块列表
- Agent 选择（auto / qa / layout / litigation）
- Query 输入
- Extra Params（country / top_k）
- Agent 运行结果：`selected_agent`、`routing_reason`、`structured_result`、`evidence`
- Benchmark 展示：summary 指标 + case 表格
- 全局错误提示
- loading 状态（配置加载、运行中、评估中）

## 前后端联调是否成功
- **成功（接口已真实联调）**
  - 前端代码调用：`GET /api/config`、`POST /api/run`、`POST /api/benchmark/run`
  - 后端真实调用结果见：
    - `outputs/config_check.json`
    - `outputs/run_qa.json`
    - `outputs/run_layout.json`
    - `outputs/run_litigation.json`
    - `outputs/benchmark_summary.json`

## 功能通过情况
- agent 选择：通过
- 输入提交：通过
- evidence 展示：通过
- routing_reason 展示：通过
- benchmark 展示：通过
- 错误提示：通过
- loading 状态：通过

## 说明
- 本环境无 browser_container 工具，无法附加浏览器截图；已完成 `vite` 编译与 dev server 启动验证。
