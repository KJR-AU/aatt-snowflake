from langchain_openai import ChatOpenAI
from langchain_classic.prompts import ChatPromptTemplate

from langchain_chroma import Chroma
from chromadb import HttpClient
from langchain_classic.schema.output_parser import StrOutputParser
from langchain.embeddings import init_embeddings
from pathlib import Path
from langchain_classic.schema.runnable import RunnablePassthrough


class RAGClient:
    """
    RAGClient connects to a ChromaDB instance (with existing or new embeddings)
    and provides:
      • retrieve() — fetch documents only
      • generate() — call the LLM directly
      • answer_from_context() — run generation using custom context
      • invoke() — full retrieval-augmented generation (RAG pipeline)
    """

    def __init__(
        self,
        temperature: float = 0.1,
        chroma_host: str = "localhost",
        chroma_port: int = 8000,
        collection_name: str = "default",
        model_name: str = "gpt-4o-mini",
        embedding_model: str = "huggingface:all-MiniLM-L6-v2",
        prompt_path: str | Path = "./prompt.txt",
        k: int = 3,
    ):
        # 1️⃣ Connect to Chroma
        self.client = HttpClient(host=chroma_host, port=chroma_port)
        print(f"✅ Connected to Chroma at http://{chroma_host}:{chroma_port}")

        # 2️⃣ Initialize embeddings (HuggingFace model)
        self.embeddings = init_embeddings(embedding_model)

        # 3️⃣ Initialize VectorStore and retriever
        self.vectordb = Chroma(
            client=self.client,
            collection_name=collection_name,
            embedding_function=self.embeddings,
        )
        self.retriever = self.vectordb.as_retriever(search_kwargs={"k": k})
        print(f"📚 Using Chroma collection: {collection_name}")

        # 4️⃣ Define prompt
        self.prompt_path: str | Path = prompt_path
        self.prompt = ChatPromptTemplate.from_template(self.load_prompt(prompt_path))

        # 5️⃣ Define LLM
        self.temperature: float = temperature
        self.model_name: str = model_name
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        print(f"🤖 LLM initialized: {model_name}")

        # 6️⃣ Build RAG pipeline
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
            {"context": self.retriever | self._combine_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    # ==============================================================
    # Independent Interfaces
    # ==============================================================

    def retrieve(self, query: str):
        """Retrieve top-k documents only (no generation)."""
        print(f"🔎 Retrieving docs for query: {query}")
        return self.retriever.invoke(query)

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
    chroma_host = "host.docker.internal"
    chroma_port = 8000
    collection_name = "aatt_practice_statements"

    rag = RAGClient(
        collection_name=collection_name,
        chroma_host=chroma_host,
        chroma_port=chroma_port,
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
