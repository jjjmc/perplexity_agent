# API 部署指南

本文档介绍如何将 Perplexity Agent 部署为 Web API 服务。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

或者使用 Poetry：

```bash
poetry add fastapi uvicorn[standard] pydantic
```

### 2. 设置环境变量

```bash
export PERPLEXITY_API_KEY="your-api-key-here"
```

或创建 `.env` 文件：

```
PERPLEXITY_API_KEY=your-api-key-here
```

### 3. 启动 API 服务

```bash
# 方式一：使用 uvicorn 命令
uvicorn perplexity_agent.api:app --host 0.0.0.0 --port 8000

# 方式二：使用 Python 模块
python -m perplexity_agent.api

# 方式三：直接运行
python -c "from perplexity_agent.api import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8000)"
```

### 4. 访问 API

- API 文档（Swagger UI）: http://localhost:8000/docs
- ReDoc 文档: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health

## API 端点

### 1. 健康检查

```bash
GET /health
```

响应：
```json
{
  "status": "healthy",
  "agent": "ready"
}
```

### 2. 简单提问

```bash
POST /ask
Content-Type: application/json

{
  "question": "What is Python?",
  "model": "sonar-reasoning",
  "temperature": 0.2
}
```

响应：
```json
{
  "answer": "Python is a high-level programming language...",
  "model": "sonar-reasoning"
}
```

### 3. 多轮对话

```bash
POST /chat
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language."},
    {"role": "user", "content": "What are its main features?"}
  ],
  "model": "sonar-reasoning"
}
```

### 4. 获取完整响应

```bash
POST /full-response
Content-Type: application/json

{
  "question": "Explain quantum computing",
  "model": "sonar-reasoning"
}
```

## 使用示例

### curl 示例

```bash
# 简单提问
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is Python?",
    "model": "sonar-reasoning"
  }'

# 多轮对话
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello!"},
      {"role": "user", "content": "What is 2+2?"}
    ]
  }'
```

### Python 示例

```python
import requests

# 简单提问
response = requests.post(
    "http://localhost:8000/ask",
    json={
        "question": "What is Python?",
        "model": "sonar-reasoning",
        "temperature": 0.2
    }
)
print(response.json())

# 多轮对话
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "messages": [
            {"role": "user", "content": "What is Python?"},
            {"role": "user", "content": "What are its features?"}
        ]
    }
)
print(response.json())
```

### JavaScript 示例

```javascript
// 使用 fetch
fetch('http://localhost:8000/ask', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    question: 'What is Python?',
    model: 'sonar-reasoning'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 生产环境部署

### 使用 systemd（Linux）

创建服务文件 `/etc/systemd/system/perplexity-agent.service`:

```ini
[Unit]
Description=Perplexity Agent API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/perplexity_agent
Environment="PATH=/opt/perplexity_agent/venv/bin"
Environment="PERPLEXITY_API_KEY=your-api-key"
ExecStart=/opt/perplexity_agent/venv/bin/uvicorn perplexity_agent.api:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl start perplexity-agent
sudo systemctl enable perplexity-agent
sudo systemctl status perplexity-agent
```

### 使用 Supervisor

创建配置文件 `/etc/supervisor/conf.d/perplexity-agent.conf`:

```ini
[program:perplexity-agent]
command=/opt/perplexity_agent/venv/bin/uvicorn perplexity_agent.api:app --host 0.0.0.0 --port 8000
directory=/opt/perplexity_agent
user=www-data
autostart=true
autorestart=true
environment=PERPLEXITY_API_KEY="your-api-key"
stdout_logfile=/var/log/perplexity-agent.log
```

启动服务：

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start perplexity-agent
```

### 使用 Nginx 反向代理

Nginx 配置示例：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 使用 Docker

创建 `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY perplexity_agent/ ./perplexity_agent/

ENV PERPLEXITY_API_KEY=""

CMD ["uvicorn", "perplexity_agent.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

构建和运行：

```bash
docker build -t perplexity-agent .
docker run -d -p 8000:8000 -e PERPLEXITY_API_KEY="your-key" perplexity-agent
```

## 性能优化

### 使用多个工作进程

```bash
uvicorn perplexity_agent.api:app --host 0.0.0.0 --port 8000 --workers 4
```

### 使用 Gunicorn + Uvicorn

```bash
pip install gunicorn
gunicorn perplexity_agent.api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 安全建议

1. **不要将 API Key 提交到代码仓库**
2. **使用环境变量管理敏感信息**
3. **在生产环境限制 CORS 来源**
4. **使用 HTTPS**
5. **设置适当的防火墙规则**
6. **考虑添加 API 认证（如 API Key 验证）**

## 故障排查

### 检查服务状态

```bash
curl http://localhost:8000/health
```

### 查看日志

如果使用 systemd：
```bash
sudo journalctl -u perplexity-agent -f
```

如果使用 Supervisor：
```bash
sudo supervisorctl tail -f perplexity-agent
```

### 常见问题

1. **API Key 未设置**: 确保设置了 `PERPLEXITY_API_KEY` 环境变量
2. **端口被占用**: 使用 `lsof -i :8000` 检查端口占用
3. **依赖未安装**: 运行 `pip install -r requirements.txt`

