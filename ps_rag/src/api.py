from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import os
from rag import RAGClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_client
    try:
        print("Initializing RAG client")
        os.getenv("OPENAI_API_KEY")  # ensures validation happens early if missing
        MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
        MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.1"))
        RETRIEVER_URL = os.getenv("RETRIEVER_URL", "http://localhost:8081")
        RETRIEVER_TIMEOUT = int(os.getenv("RETRIEVER_TIMEOUT", "30"))
        RETRIEVER_K = int(os.getenv("RETRIEVER_K", "3"))
        rag_client = RAGClient(
            temperature=MODEL_TEMPERATURE,
            model_name=MODEL_NAME,
            prompt_path="./prompt.txt",
            k=RETRIEVER_K,
            retriever_url=RETRIEVER_URL,
            retriever_timeout=RETRIEVER_TIMEOUT,
        )
        app.state.rag_client = rag_client
        print("🚀 RAGClient initialized successfully.")
    except Exception as e:
        print(f"❌ Failed to initialize RAGClient: {e}")
        raise e
    yield
    print("Shutting down")

app = FastAPI(
    title="RAG Service",
    description="A simple FastAPI wrapper around a LangChain RAG client using the retriever microservice",
    version="1.0.0",
    lifespan=lifespan
)

class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    query: str
    answer: str

@app.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    """
    POST /query
    {
        "query": "What is the current ICU occupancy rate?"
    }
    """
    if not hasattr(app.state, "rag_client") and "rag_client" not in globals():
        raise HTTPException(status_code=500, detail="RAGClient not initialized")

    try:
        answer = rag_client.invoke(request.query)
        return QueryResponse(query=request.query, answer=answer)

    except Exception as e:
        print(f"❌ RAG invocation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def health():
    return {"status": "ok", "message": "RAG service running"}
