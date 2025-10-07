from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from session import session

class SimpleRag:

    def __init__(self, top_k: int = 3, model: str = "gpt-4o-mini", temperature: float = 0):
        self.top_k = top_k
        self.model = model
        self.temperature = temperature
        self.llm = ChatOpenAI(model=self.model, temperature=self.temperature)

    def retrieve(self, query: str):
        sql_query = """
            with results as 
            (select file_path, VECTOR_COSINE_SIMILARITY(vector_db.chunk_vec,
            SNOWFLAKE.CORTEX.EMBED_TEXT_768('e5-base-v2', ?)) as similarity, chunk
            from vector_db
            order by similarity desc
            limit ?)
            select chunk, similarity, file_path from results 
            """
        return [row.CHUNK for row in session.sql(sql_query, [query, self.top_k]).collect()]

    def generate(self, query: str) -> str:
        # Retrieve top-k relevant chunks
        chunks = self.retrieve(query)
        context = "\n\n".join(chunks)

        # Build a simple RAG prompt
        prompt_template = PromptTemplate.from_template("""
        You are an assistant that answers questions based only on the provided context.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """)

        # Format the final prompt
        prompt = prompt_template.format(context=context, question=query)

        # Run the LLM
        response = self.llm.invoke(prompt)
        return response.content


if __name__ == "__main__":
    rag = SimpleRag(top_k=2, model="gpt-4o-mini", temperature=0)

    query = "What are the key points about Arissian Ltd's AE proposal?"
    response = rag.generate(query)
    print(response)