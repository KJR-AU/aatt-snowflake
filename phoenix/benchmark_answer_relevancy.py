from client import client
from metrics.deepeval import answer_relevance_evaluator
import json

DATASET_NAME: str = "answer-relevancy-20"
DATASET_PATH: str = "./datasets/benchmarks/answer_relevancy/answer_relevancy.csv"
EXPERIMENT_NAME: str = "deepeval-answer-relevancy-test"

def dummy_task(input, reference):
    """Pass through the reference so that the metric can accept it as an 'output'.
    """
    return list(reference.values())[0]

try:
    print(f"Creating dataset: {DATASET_NAME}")
    dataset = client.datasets.create_dataset(
        csv_file_path=DATASET_PATH,
        name=DATASET_NAME,
        input_keys=["input"], # corresponds to input parameter in experiments
        output_keys=["output"], # corresponds to reference parameter in experiments
        metadata_keys=["expected_score"]
    )
except:
    print(f"Loading dataset: {DATASET_NAME}")
    dataset = client.datasets.get_dataset(
        dataset=DATASET_NAME
    )

client.experiments.run_experiment(
    dataset=dataset,
    task=dummy_task,
    evaluators=[answer_relevance_evaluator],
    experiment_name=EXPERIMENT_NAME
)