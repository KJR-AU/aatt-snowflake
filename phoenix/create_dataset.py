from client import client

DATASET_NAME: str = "my-dataset"
DATASET_PATH: str = "../eval/evaluations/ragas/datasets/dataset1.csv"

dataset = client.datasets.create_dataset(
    csv_file_path="../eval/evaluations/ragas/datasets/dataset1.csv",
    name=DATASET_NAME,
    input_keys=["user_input"], # corresponds to input parameter in experiments
    output_keys=["reference"] # corresponds to reference parameter in experiments
)
print(dataset)