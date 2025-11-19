# PS RAG Helm Chart

This chart packages the AATT Practice Statement RAG API, its Chroma vector database, and the job that builds the vector store. Environment variables for each workload are defined in `values.yaml`, so you can supply a custom `values.yml` (or `values-<env>.yaml`) when installing the chart. The OpenAI API key only needs to be set once via `global.openai.apiKey`.

## Usage

```bash
cd ps_rag/chart
helm install ps-rag ./ps-rag -f my-values.yaml
```

### Customizing environment variables

Update (or override) the `api.env`, `chroma.env`, and `builderJob.env` sections in your values file, and provide the API key once at the `global` level:

```yaml
global:
  openai:
    apiKey: "your-key"

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
  env:
    CHROMA_SERVER_HOST: 0.0.0.0
    CHROMA_SERVER_PORT: "8000"
    IS_PERSISTENT: "TRUE"
    PERSIST_DIRECTORY: /data
  persistence:
    storageClass: gp2
    size: 5Gi
```

Set other knobs (replica counts, images, serviceAccount, persistence) in the same values file as needed.
