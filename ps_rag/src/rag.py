from __future__ import annotations

from pathlib import Path
from typing import Any, List

from langchain_openai import ChatOpenAI
from langchain_classic.prompts import ChatPromptTemplate
from langchain_classic.schema.output_parser import StrOutputParser
from langchain_classic.schema.runnable import RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda

from client import PracticeStatementRetrieverClient


class RAGClient:
    """
    RAGClient now delegates document retrieval to the retriever microservice.
    It still provides:
      • retrieve() — fetch documents only
      • generate() — call the LLM directly
      • answer_from_context() — run generation using custom context
      • invoke() — full retrieval-augmented generation (RAG pipeline)
    """

    def __init__(
        self,
        temperature: float = 0.1,
        model_name: str = "gpt-4o-mini",
        prompt_path: str | Path = "./prompt.txt",
        k: int = 3,
        retriever_url: str = "http://localhost:8081",
        retriever_timeout: int = 30,
    ):
        # Retriever microservice client
        self.k = k
        self.retriever_timeout = retriever_timeout
        self.retriever_client = PracticeStatementRetrieverClient(retriever_url)
        print(f"🔌 Using retriever at {retriever_url}")

        # Prompt definition
        self.prompt_path: str | Path = prompt_path
        self.prompt = ChatPromptTemplate.from_template(self.load_prompt(prompt_path))

        # LLM setup
        self.temperature: float = temperature
        self.model_name: str = model_name
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        print(f"🤖 LLM initialized: {model_name}")

        # Build pipeline
        self.retriever_runnable = RunnableLambda(self._retrieve_documents)
        self.rag_chain = self._build_chain()

    # --- Helper to combine retrieved docs ---
    @staticmethod
    def _combine_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def load_prompt(self, file_path: str | Path):
        if not isinstance(file_path, Path):
            file_path = Path(file_path)
        with file_path.open() as f:
            return f.read()

    # --- Build the RAG pipeline ---
    def _build_chain(self):
        return (
            {"context": self.retriever_runnable | self._combine_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def _retrieve_documents(self, query: str):
        docs_payload = self.retriever_client.retrieve(
            query,
            top_k=self.k,
            timeout=self.retriever_timeout,
        )
        return self._to_langchain_documents(docs_payload)

    @staticmethod
    def _to_langchain_documents(docs_payload: List[dict[str, Any]]) -> List[Document]:
        return [
            Document(page_content=doc.get("page_content", ""), metadata=doc.get("metadata") or {})
            for doc in docs_payload
        ]

    # ==============================================================
    # Independent Interfaces
    # ==============================================================

    def retrieve(self, query: str, top_k: int | None = None):
        """Retrieve top-k documents only (no generation)."""
        print(f"🔎 Retrieving docs for query: {query}")
        docs_payload = self.retriever_client.retrieve(
            query,
            top_k=top_k or self.k,
            timeout=self.retriever_timeout,
        )
        return self._to_langchain_documents(docs_payload)

    def generate(self, prompt: str):
        """Call the LLM directly with a plain text prompt."""
        print("💬 Generating output directly from LLM...")
        response = self.llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)

    def answer_from_context(self, query: str, docs):
        """Run the generation step manually with provided context documents."""
        context = self._combine_docs(docs)
        formatted_prompt = self.prompt.format(context=context, question=query)
        return self.generate(formatted_prompt)

    def invoke(self, query: str):
        """Full RAG pipeline: retrieval → generation."""
        print(f"⚙️ Running full RAG pipeline for: {query}")
        return self.rag_chain.invoke(query)


# ==============================================================
# Example Usage
# ==============================================================

if __name__ == "__main__":
    rag = RAGClient(
        retriever_url="http://localhost:8081",
    )

    query = "Summarise the offerings of the provider AgeChecked"

    # --- Example 1: Retrieve only
    docs = rag.retrieve(query)
    print(f"\n📄 Retrieved {len(docs)} documents:")
    for d in docs:
        print("-", d.page_content[:100], "...")

    # --- Example 2: Generate directly
    summary_prompt = "Explain the role of age verification in digital safety."
    result_llm = rag.generate(summary_prompt)
    print("\n🧠 LLM Direct Output:\n", result_llm)

    # --- Example 3: Combine manually (retrieved docs + LLM)
    result_combined = rag.answer_from_context(query, docs)
    print("\n🧩 Answer from context:\n", result_combined)

    # --- Example 4: Full RAG pipeline
    result_full = rag.invoke(query)
    print("\n💬 Question:", query)
    print("🧠 Full RAG Answer:", result_full)
