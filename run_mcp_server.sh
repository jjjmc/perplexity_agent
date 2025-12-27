#!/bin/bash
# 启动 Perplexity Agent MCP Server

set -e

echo "🚀 启动 A2Z Perplexity Agent MCP Server..."
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    exit 1
fi

# 检查 API key
if [ -z "$PERPLEXITY_API_KEY" ]; then
    if [ -f .env ]; then
        echo "📝 从 .env 文件加载配置..."
        export $(cat .env | grep -v '^#' | xargs)
    else
        echo "❌ 错误: 未设置 PERPLEXITY_API_KEY 环境变量"
        echo ""
        echo "请选择以下方式之一设置 API key:"
        echo "1. 设置环境变量: export PERPLEXITY_API_KEY='your-api-key'"
        echo "2. 创建 .env 文件: echo 'PERPLEXITY_API_KEY=your-api-key' > .env"
        exit 1
    fi
fi

# 设置默认端口
PORT=${1:-7004}

# 检查端口是否被占用
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  警告: 端口 $PORT 已被占用"
    read -p "是否要停止占用端口的进程? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        lsof -ti:$PORT | xargs kill -9
        sleep 1
    else
        echo "请使用其他端口或停止占用端口的进程"
        exit 1
    fi
fi

# 启动服务
echo ""
echo "✅ 配置检查完成"
echo "📍 MCP 地址: http://0.0.0.0:$PORT/mcp"
echo "📍 本地访问: http://127.0.0.1:$PORT/mcp"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 启动服务
uvicorn server:app --host 0.0.0.0 --port $PORT

