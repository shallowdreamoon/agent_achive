# Docker Verification (2026-04-07 UTC)

执行命令：
```bash
docker compose up --build
```

## 结果
- compose 是否能启动：**否**
- 原因：当前执行环境不存在 `docker` 命令（`/bin/bash: docker: command not found`）
- backend 8000 监听：**无法验证（受上述限制）**
- frontend 5173 监听：**无法验证（受上述限制）**

## .env 要求
- 已新增 `.env.example`，默认可离线演示：
  - `MOCK_MODE=true`
  - `ENABLE_REMOTE_EMBEDDING=false`
- Real LLM 模式：
  - `MOCK_MODE=false`
  - 配置 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL`

## 无 API Key 的 demo 启动方式
- 使用 mock 模式（`.env` 复制 `.env.example` 即可）
