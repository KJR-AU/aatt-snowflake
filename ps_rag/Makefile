build:
	docker build -t aatt-ps-rag-api .
	docker build -t aatt-ps-rag-build-vector-db -f Dockerfile-vectordb .
	docker build -t aatt-ps-rag-retriever -f Dockerfile-retriever .
	helm upgrade --install aatt-ps-rag ./chart/ps-rag -f helm-values.yml