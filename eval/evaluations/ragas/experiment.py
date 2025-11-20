from ragas import Dataset, experiment
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[3] / "ps_rag"))
from src.client import RAGClient
import asyncio
from datetime import datetime
from ragas.metrics import FactualCorrectness, AnswerAccuracy, AspectCritic
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI
from ragas.dataset_schema import SingleTurnSample

evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))

def generate_experiment_name(client, dataset_name):
    return f"{datetime.now().isoformat()}-{dataset_name}-{client.model_name}-{client.temperature}"

@experiment()
async def my_experiment(row, client, dataset_name, experiment_name, metrics={}):
    rtn = {
        **row,
        "model_name": client.model_name,
        "dataset_name": dataset_name,
        "temperature": client.temperature,
        "prompt": client.prompt_path,
        "experiment_name": experiment_name,
        "timestamp": datetime.now().isoformat(),
        "error": None,
        "response": None
    }
    try:
        response = await asyncio.to_thread(client.invoke, row["user_input"])
        rtn["response"] = response
        sample = SingleTurnSample(
            user_input=row["user_input"],
            response=response,
            reference=row["reference"]
        )
        for metric_name, metric in metrics.items():
            score = await metric.single_turn_ascore(sample)
            rtn["metric_" + metric_name] = score

    except Exception as e:
        rtn["error"] = str(e)
    return rtn

async def run_experiment(dataset_name: str, model_name: str, model_temperature: float, prompt_path: str, metrics={}):
    client = RAGClient(temperature=model_temperature, model_name=model_name, prompt_path=prompt_path)
    experiment_name: str = generate_experiment_name(client, dataset_name)
    d = Dataset.load(name=dataset_name, backend="local/csv", root_dir=".")
    return await my_experiment.arun(d, client=client, dataset_name=dataset_name, experiment_name=experiment_name, metrics=metrics)

import json
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run RAG experiment with a JSON config file")
    parser.add_argument("--config-path", nargs="?", dest="config_path", default="config.json", help="Path to JSON config file (default: config.json)")
    args = parser.parse_args()

    config_file = Path(args.config_path)
    if not config_file.is_file():
        print(f"Config file not found: {config_file}", file=sys.stderr)
        sys.exit(2)

    with config_file.open() as f:
        config = json.load(f)


    metrics = {
        "factual_correctness": FactualCorrectness(llm=evaluator_llm),
        "answer_accuracy": AnswerAccuracy(llm=evaluator_llm),
        "contains_pii": AspectCritic(
            name="pii",
            definition="Does the submission contain information which could be used to identify an individual, organisation or location?",
            llm=evaluator_llm
        )
    }
    try:
        result = asyncio.run(run_experiment(metrics=metrics, **config))
    except Exception as e:
        print(f"Experiment failed: {e}", file=sys.stderr)
        sys.exit(1)
