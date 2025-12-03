## Define an evaluator using a RAGAS metric: answer accuracy
from ragas.metrics import ContextRelevance
from ragas.dataset_schema import SingleTurnSample
from .model import evaluation_llm

ragas_context_relevance_scorer = ContextRelevance(llm=evaluation_llm)

def context_relevance_evaluator(input, output):
    retrieved_contexts = [doc['page_content'] for doc in output]
    sample = SingleTurnSample(
        user_input=list(input.values())[0],
        retrieved_contexts=retrieved_contexts
    )
    return ragas_context_relevance_scorer.single_turn_score(sample)