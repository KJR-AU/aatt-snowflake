import sys
sys.path.append("..")
from ps_rag.src.client import PracticeStatementRagClient

rag = PracticeStatementRagClient("http://localhost:8080")

## Define our practice statement RAG task
## To understand how task and evaluator functions work see: 
## https://arize-phoenix.readthedocs.io/projects/client/en/latest/api/experiments.html#client.resources.experiments.Experiments.run_experiment
def ps_rag_task(input):
    query = list(input.values())[0]
    # Because we've include 'input' as a named parameter, the input value
    # defined on the dataset will be passed to this function when invoked.
    return rag.invoke(query)