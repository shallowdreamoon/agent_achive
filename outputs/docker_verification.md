# Docker Verification (2026-04-07 UTC)

## 是否真实执行过 `docker compose up --build`
- 已执行：`docker compose up --build`

## 是否成功
- **失败**

## 失败点
- 当前环境缺少 Docker CLI：`docker: command not found`
- 因此无法在本环境验证容器内 backend/frontend 监听端口。

## mock 模式怎么启动
1. `cp .env.example .env`
2. 保持 `.env` 中：
   - `MOCK_MODE=true`
   - `ENABLE_REMOTE_EMBEDDING=false`
3. 执行：`docker compose up --build`

## real LLM 模式怎么启动
1. `cp .env.example .env`
2. 修改 `.env`：
   - `MOCK_MODE=false`
   - `OPENAI_API_KEY=<your-key>`
   - `OPENAI_BASE_URL=<compatible-base-url>`（可保留默认）
   - `OPENAI_MODEL=<model-name>`
3. 执行：`docker compose up --build`
