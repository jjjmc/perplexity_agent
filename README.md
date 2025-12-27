# A2Z Perplexity Agent (MCP)

一个基于 MCP (Model Context Protocol) 的 Perplexity AI 搜索 Agent，提供强大的网络搜索和信息查询能力。

## 功能特性

- 🔍 实时网络搜索
- 💬 多轮对话支持
- 📊 完整响应（包含引用和元数据）
- 🚀 基于 MCP 协议，易于集成

## 安装

### 使用 pip

```bash
pip install -r requirements.txt
```

### 使用 Poetry

```bash
poetry install
```

## 配置

### 环境变量（可选）

如果未设置环境变量，将使用默认的 API key。

```bash
export PERPLEXITY_API_KEY="your_api_key_here"
```

或者在 `.env` 文件中：

```
PERPLEXITY_API_KEY=your_api_key_here
```

## MCP Server 使用

### 启动 MCP 服务器

```bash
# 方式1: 使用启动脚本（推荐）
bash run_mcp_server.sh [port]

# 方式2: 使用 uvicorn
uvicorn server:app --host 0.0.0.0 --port 7004

# 方式3: 直接运行
python server.py --port 7004
```

### MCP 接口地址

- 本地: `http://127.0.0.1:7004/mcp`
- 生产环境: `https://agent.deepnlp.org/container/aiagenta2z/perplexity_agent/mcp`

### 提供的 MCP Tools

1. **perplexity_search**: 简单搜索，返回文本答案
   - 参数: `question` (必需), `model`, `temperature`, `max_tokens`
   - 返回: 包含答案、模型、问题和状态消息的字典

2. **perplexity_chat**: 多轮对话
   - 参数: `messages` (必需), `model`, `temperature`, `max_tokens`
   - 返回: 包含完整响应、答案、模型和状态消息的字典

3. **perplexity_search_full**: 完整响应（包含元数据、引用等）
   - 参数: `question` (必需), `model`, `temperature`, `max_tokens`
   - 返回: 包含完整 API 响应、答案、模型、问题和状态消息的字典

### MCP 使用示例

通过 MCP 客户端调用：

```python
# 简单搜索
result = mcp_client.call_tool("perplexity_search", {
    "question": "What is the latest news about AI?",
    "model": "sonar-reasoning"
})

# 多轮对话
result = mcp_client.call_tool("perplexity_chat", {
    "messages": [
        {"role": "user", "content": "What is Python?"},
        {"role": "assistant", "content": "Python is a programming language."},
        {"role": "user", "content": "What are its main features?"}
    ]
})

# 获取完整响应（包含引用和元数据）
result = mcp_client.call_tool("perplexity_search_full", {
    "question": "Explain quantum computing",
    "model": "sonar-reasoning"
})
```

## 支持的模型

- `sonar-reasoning` (默认)
- `sonar`
- `llama-3.1-sonar-small-128k-online`
- `llama-3.1-sonar-large-128k-online`
- `llama-3.1-sonar-huge-128k-online`

## 项目结构

```
perplexity_agent/
├── perplexity_agent/
│   ├── __init__.py      # 包初始化
│   ├── agent.py         # 核心 Agent 类
│   └── agent.json       # Agent 配置
├── server.py            # MCP 服务器主文件
├── run_mcp_server.sh    # MCP 服务器启动脚本
├── requirements.txt     # pip 依赖文件
├── pyproject.toml       # Poetry 配置文件
├── README.md           # 项目文档
└── .gitignore          # Git 忽略文件
```

## 开发

### 安装开发依赖

```bash
poetry install --with dev
```

### 代码格式化

```bash
poetry run black .
poetry run ruff check .
```

### 类型检查

```bash
poetry run mypy perplexity_agent
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
