# Perplexity Agent

一个支持外部调用的 Perplexity AI Agent，提供简单易用的 Python API 和命令行工具。

## 功能特性

- 🚀 简单易用的 Python API
- 💻 命令行工具支持
- 🔧 灵活的配置选项
- 📝 完整的类型提示支持
- 🛡️ 完善的错误处理

## 安装

### 使用 Poetry（推荐）

```bash
# 安装 Poetry（如果还没有安装）
curl -sSL https://install.python-poetry.org | python3 -

# 安装依赖
poetry install
```

### 使用 pip

```bash
pip install -e .
```

## 配置

### 环境变量

创建 `.env` 文件或设置环境变量：

```bash
export PERPLEXITY_API_KEY="your_api_key_here"
```

或者在 `.env` 文件中：

```
PERPLEXITY_API_KEY=your_api_key_here
```

## 使用方法

### Python API

#### 基本使用

```python
from perplexity_agent import PerplexityAgent

# 初始化 agent（API key 从环境变量读取）
agent = PerplexityAgent()

# 简单提问
answer = agent.ask("What is the capital of France?")
print(answer)

# 获取完整响应
full_response = agent.get_full_response("Explain quantum computing")
print(full_response)
```

#### 自定义参数

```python
agent = PerplexityAgent(api_key="your-api-key")

# 使用自定义参数
answer = agent.ask(
    question="Write a poem about AI",
    model="sonar-reasoning",
    temperature=0.7,
    max_tokens=200,
)
```

#### 多轮对话

```python
messages = [
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language."},
    {"role": "user", "content": "What are its main features?"},
]

response = agent.chat(messages=messages)
print(response["choices"][0]["message"]["content"])
```

### 命令行工具

#### 基本使用

```bash
# 使用命令行参数
perplexity-agent "What is the capital of France?"

# 从标准输入读取
echo "What is Python?" | perplexity-agent

# 使用管道
cat question.txt | perplexity-agent
```

#### 高级选项

```bash
# 指定模型
perplexity-agent "Explain AI" --model sonar-reasoning

# 调整温度参数
perplexity-agent "Write a poem" --temperature 0.7

# 限制最大 token 数
perplexity-agent "Summarize this" --max-tokens 200

# 输出完整 JSON 响应
perplexity-agent "What is Python?" --full-response

# 指定 API key
perplexity-agent "Hello" --api-key your-api-key
```

## 示例

运行示例代码：

```bash
poetry run python example.py
```

或者：

```bash
python example.py
```

## API 参考

### PerplexityAgent

#### `__init__(api_key=None, base_url=None)`

初始化 Perplexity Agent。

**参数：**
- `api_key` (str, optional): Perplexity API key。如果不提供，将从环境变量 `PERPLEXITY_API_KEY` 读取。
- `base_url` (str, optional): API 基础 URL。默认为 Perplexity chat completions 端点。

#### `ask(question, model="sonar-reasoning", temperature=0.2, max_tokens=None, **kwargs)`

提问并获取文本回答。

**参数：**
- `question` (str): 要问的问题。
- `model` (str): 使用的模型。默认为 `sonar-reasoning`。
- `temperature` (float): 采样温度（0.0 到 1.0）。默认为 0.2。
- `max_tokens` (int, optional): 生成的最大 token 数。
- `**kwargs`: 传递给 API 的额外参数。

**返回：**
- `str`: 助手的文本回答。

#### `get_full_response(question, model="sonar-reasoning", temperature=0.2, max_tokens=None, **kwargs)`

提问并获取完整的 API 响应。

**参数：**
- 同 `ask()` 方法。

**返回：**
- `dict`: 完整的 API 响应字典。

#### `chat(messages, model="sonar-reasoning", temperature=0.2, max_tokens=None, **kwargs)`

发送聊天完成请求到 Perplexity API。

**参数：**
- `messages` (List[Dict[str, str]]): 消息列表，每个消息包含 `role` 和 `content` 键。
- 其他参数同 `ask()` 方法。

**返回：**
- `dict`: API 响应字典。

## 项目结构

```
perplexity_agent/
├── perplexity_agent/
│   ├── __init__.py      # 包初始化
│   ├── agent.py         # 核心 Agent 类
│   └── cli.py           # 命令行接口
├── example.py           # 使用示例
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

### 运行测试

```bash
poetry run pytest
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
