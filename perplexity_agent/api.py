"""FastAPI Web API for Perplexity Agent."""

from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from perplexity_agent.agent import PerplexityAgent

app = FastAPI(
    title="Perplexity Agent API",
    description="RESTful API for Perplexity AI Agent",
    version="0.1.0",
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局 agent 实例
agent: Optional[PerplexityAgent] = None


@app.on_event("startup")
async def startup_event() -> None:
    """初始化 agent 实例."""
    global agent
    try:
        agent = PerplexityAgent()
    except ValueError as e:
        raise RuntimeError(f"Failed to initialize PerplexityAgent: {e}") from e


# 请求模型
class QuestionRequest(BaseModel):
    """提问请求模型."""

    question: str = Field(..., description="要问的问题", min_length=1)
    model: Optional[str] = Field(default="sonar-reasoning", description="使用的模型")
    temperature: Optional[float] = Field(default=0.2, ge=0.0, le=1.0, description="采样温度")
    max_tokens: Optional[int] = Field(default=None, ge=1, description="最大 token 数")


class ChatRequest(BaseModel):
    """聊天请求模型."""

    messages: List[Dict[str, str]] = Field(..., description="消息列表")
    model: Optional[str] = Field(default="sonar-reasoning", description="使用的模型")
    temperature: Optional[float] = Field(default=0.2, ge=0.0, le=1.0, description="采样温度")
    max_tokens: Optional[int] = Field(default=None, ge=1, description="最大 token 数")


# 响应模型
class AnswerResponse(BaseModel):
    """回答响应模型."""

    answer: str = Field(..., description="助手的回答")
    model: str = Field(..., description="使用的模型")


class FullResponse(BaseModel):
    """完整响应模型."""

    response: Dict[str, Any] = Field(..., description="完整的 API 响应")


@app.get("/")
async def root() -> Dict[str, str]:
    """根路径."""
    return {"name": "Perplexity Agent API", "version": "0.1.0", "status": "running"}


@app.get("/health")
async def health() -> Dict[str, str]:
    """健康检查."""
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    return {"status": "healthy", "agent": "ready"}


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest) -> AnswerResponse:
    """提问并获取文本回答."""
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    try:
        answer = agent.ask(
            question=request.question,
            model=request.model or "sonar-reasoning",
            temperature=request.temperature or 0.2,
            max_tokens=request.max_tokens,
        )
        return AnswerResponse(answer=answer, model=request.model or "sonar-reasoning")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get answer: {str(e)}") from e


@app.post("/chat", response_model=FullResponse)
async def chat(request: ChatRequest) -> FullResponse:
    """发送聊天完成请求."""
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    try:
        response = agent.chat(
            messages=request.messages,
            model=request.model or "sonar-reasoning",
            temperature=request.temperature or 0.2,
            max_tokens=request.max_tokens,
        )
        return FullResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to chat: {str(e)}") from e


@app.post("/full-response", response_model=FullResponse)
async def get_full_response(request: QuestionRequest) -> FullResponse:
    """提问并获取完整的 API 响应."""
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    try:
        response = agent.get_full_response(
            question=request.question,
            model=request.model or "sonar-reasoning",
            temperature=request.temperature or 0.2,
            max_tokens=request.max_tokens,
        )
        return FullResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get full response: {str(e)}") from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

