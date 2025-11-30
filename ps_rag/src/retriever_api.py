from contextlib import asynccontextmanager
import os
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chromadb import HttpClient
from langchain_chroma import Chroma
from langchain.embeddings import init_embeddings


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        chroma_host = os.getenv("CHROMA_HOST", "localhost")
        chroma_port = int(os.getenv("CHROMA_PORT", "8000"))
        collection_name = os.getenv("COLLECTION_NAME", "aatt_practice_statements")
        embedding_model = os.getenv("EMBEDDING_MODEL", "openai:text-embedding-3-large")
        default_k = int(os.getenv("RETRIEVER_K", "3"))

        client = HttpClient(host=chroma_host, port=chroma_port)
        embeddings = init_embeddings(embedding_model)
        vectordb = Chroma(
            client=client,
            collection_name=collection_name,
            embedding_function=embeddings,
        )

        app.state.vectordb = vectordb
        app.state.default_k = default_k
        print(
            f"📚 Retriever ready (collection={collection_name}, host={chroma_host}:{chroma_port}, k={default_k})"
        )
    except Exception as exc:  # pragma: no cover - fail fast during init
        print(f"❌ Failed to initialize retriever: {exc}")
        raise
    yield
    print("Retriever service shutting down.")


app = FastAPI(
    title="Chroma Retriever API",
    description="Lightweight wrapper that exposes Chroma similarity search over HTTP.",
    version="1.0.0",
    lifespan=lifespan,
)


class RetrieveRequest(BaseModel):
    query: str
    top_k: int | None = None


class RetrievedDocument(BaseModel):
    page_content: str
    metadata: dict[str, Any]


class RetrieveResponse(BaseModel):
    documents: list[RetrievedDocument]


@app.post("/retrieve", response_model=RetrieveResponse)
def retrieve_documents(request: RetrieveRequest):
    if not hasattr(app.state, "vectordb"):
        raise HTTPException(status_code=500, detail="Retriever not initialized")

    top_k = request.top_k or getattr(app.state, "default_k", 3)
    if top_k <= 0:
        raise HTTPException(status_code=400, detail="top_k must be greater than zero")

    try:
        docs = app.state.vectordb.similarity_search(request.query, k=top_k)
    except Exception as exc:
        print(f"❌ Retrieval failed: {exc}")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return RetrieveResponse(
        documents=[
            RetrievedDocument(
                page_content=doc.page_content,
                metadata=doc.metadata or {},
            )
            for doc in docs
        ]
    )


@app.get("/")
def health():
    return {"status": "ok", "message": "Retriever service running"}
