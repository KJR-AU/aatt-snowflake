from tasks import ps_retriever_task
from metrics.ragas import context_relevance_evaluator
from client import client

DATASET_NAME: str = "test-dataset3"
dataset = client.datasets.get_dataset(dataset=DATASET_NAME)

client.experiments.run_experiment(
    dataset=dataset,
    task=ps_retriever_task,
    evaluators=[context_relevance_evaluator]
)
