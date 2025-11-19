# Practice Statement RAG

This project provides a **Retrieval-Augmented Generation (RAG)** API built using **FastAPI** and backed by a **Chroma** vector database.  
It allows you to submit a query, retrieve relevant documents from a vector store, and receive an AI-generated answer grounded in those retrieved documents.

The repository includes:

- The FastAPI application  
- The tools required to build the vector database  
- A Helm chart for deploying the entire stack  
- A Python client to interact with the running API  

This README is written to be **beginner friendly** and explains how to deploy and test the application from scratch.

---

## 📁 Repository Overview

| Directory / File | Purpose |
|------------------|---------|
| `src/` | FastAPI RAG service (`api.py`) and LangChain logic |
| `docs/` + `build_vector_db.py` | Tools to load PDF/DOCX files into Chroma |
| `chart/ps-rag/` | Helm chart that deploys Chroma, the API, and the optional vector-builder Job |
| `Dockerfile`, `Dockerfile-vectordb` | Container images for the API and vector database builder |
| `client/` | Python client for querying the deployed API |
| `helm-values.yml` | Example values file for Helm |

---

# 🚀 Deploying with Helm (Recommended)

The easiest way to deploy ChromaDB + the FastAPI RAG service is using Helm.

## 1. Build the images
```bash
docker build -t aatt-ps-rag .
docker build -t aatt-ps-rag-build-vector-db -f Dockerfile-vectordb .
```

## 2. Create a Helm values file

Create `my-values.yml`:

```yaml
global:
  openai:
    apiKey: "sk-..."   # Your OpenAI key (do NOT commit real secrets)

api:
  env:
    CHROMA_HOST: chroma-service
    CHROMA_PORT: "8000"
    MODEL_NAME: gpt-4o-mini
    EMBEDDING_MODEL: huggingface:all-MiniLM-L6-v2

builderJob:
  env:
    CHROMA_HOST: chroma-service
    CHROMA_PORT: "8000"
    COLLECTION_NAME: aatt_practice_statements

chroma:
  persistence:
    storageClass: hostpath
    size: 2Gi
```

This file configures:

* The OpenAI model and embeddings
* Chroma connection details
* The vector-building job (optional)
* Persistent storage for Chroma

---

## 3. Deploy the stack using Helm

From inside the `ps_rag/` directory:

```bash
helm upgrade --install aatt-ps-rag ./chart/ps-rag -f my-values.yml
```

Helm will install:

* **ChromaDB Deployment + Service**
* **FastAPI RAG Deployment**
* **Optional vector-builder Job** (runs once to populate Chroma)

Check the deployment:

```bash
kubectl get pods
```

If the builder job is enabled:

```bash
kubectl logs job/ps-rag-builder
```

---

# 🔌 Access the API from Your Local Machine

Forward port **8080** from the Kubernetes API deployment:

```bash
kubectl port-forward deploy/ps-rag-api 8080:8080
```

The API is now available at:

```
http://localhost:8080/query
```

---

# 🧪 Test the Deployment

Run a basic test using `curl`:

```bash
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Summarise the offerings of AgeChecked"}'
```

Expected response:

```json
{
  "answer": "AgeChecked provides age assurance solutions ...",
  "sources": [...],
  "context_used": "..."
}
```

If something seems wrong, inspect logs:

```bash
kubectl logs deploy/ps-rag-api
kubectl logs job/ps-rag-builder
```

---

# 🐍 Optional: Python Client

A minimal SDK is provided:

```python
from ps_rag import PracticeStatementRagClient

client = PracticeStatementRagClient("http://localhost:8080")
response = client.invoke("Summarize the ICAP waiver requirements.")
print(response)
```
