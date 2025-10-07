from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import SnowflakeVectorStore
from langchain_community.embeddings import OpenAIEmbeddings  # or reuse Cortex embeddings

import os
from session import session

# ----------------------------
# 2. Initialize Vector Store
# ----------------------------
vectorstore = SnowflakeVectorStore(
    session=session,
    table="VECTOR_DB",
    embedding_column="CHUNK_VEC",
    text_column="CHUNK",
    metadata_columns=["FILE_PATH"],   # optional
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# ----------------------------
# 3. Define LLM
# ----------------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ----------------------------
# 4. Build RetrievalQA Chain
# ----------------------------
template = """
You are an assistant that answers based on provided context.

Context:
{context}

Question:
{question}

Answer in clear, concise language.
"""
prompt = PromptTemplate.from_template(template)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",  # can also use "map_reduce" for longer docs
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=True,
)

# ----------------------------
# 5. Run a query
# ----------------------------
query = "What do the practice statements say about risk management?"
result = qa.invoke(query)

print("Answer:", result["result"])
print("\nSources:")
for doc in result["source_documents"]:
    print("-", doc.metadata.get("FILE_PATH"))
