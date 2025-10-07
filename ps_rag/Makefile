build_infra:
	cd terraform && terraform init && terraform apply -auto-approve

stage:
	python stage_docs.py

build_vector_db:
	python build_vector_db.py