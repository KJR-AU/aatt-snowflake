from client import client
import asyncio

async def main():
    dataset = await client.datasets.create_dataset(
        csv_file_path="../eval/evaluations/ragas/datasets/dataset1.csv",
        name="test-dataset",
        input_keys=["user_input"],
        output_keys=["reference"]
    )

asyncio.run(main())