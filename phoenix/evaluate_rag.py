from client import client
import sys
sys.path.append("..")
from ps_rag.src.client import PracticeStatementRagClient
from metrics.ragas import answer_accuracy_evaluator
from metrics.phoenix import spelling_evaluator
from metrics.deepeval import answer_relevance_evaluator
from tasks import ps_rag_task

DATASET_NAME: str = "test-dataset3"
dataset = client.datasets.get_dataset(dataset=DATASET_NAME)
client.experiments.run_experiment(
    dataset=dataset, 
    task=ps_rag_task, 
    evaluators=[
        answer_relevance_evaluator,
        spelling_evaluator,
        answer_accuracy_evaluator
    ]
)