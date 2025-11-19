from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import os
from client import RAGClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_client
    try:
        print("Initializing RAG client")
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
        CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
        COLLECTION_NAME = os.getenv("COLLECTION_NAME", "aatt_practice_statements")
        MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
        EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "huggingface:all-MiniLM-L6-v2")
        rag_client = RAGClient(
            chroma_host=CHROMA_HOST,
            chroma_port=CHROMA_PORT,
            collection_name=COLLECTION_NAME,
            model_name=MODEL_NAME,
            embedding_model=EMBEDDING_MODEL,
            prompt_path="./prompt.txt",
            k=3
        )
        print("🚀 RAGClient initialized successfully.")
    except Exception as e:
        print(f"❌ Failed to initialize RAGClient: {e}")
        raise e
    yield
    print("Shutting down")

app = FastAPI(
    title="RAG Service",
    description="A simple FastAPI wrapper around a LangChain RAG client using ChromaDB",
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
