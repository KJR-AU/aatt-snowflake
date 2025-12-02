## Define an evaluator using a RAGAS metric: answer accuracy
from ragas.metrics import AnswerAccuracy
from ragas.llms import llm_factory
from ragas.dataset_schema import SingleTurnSample
import os

evaluation_model_name: str = os.getenv("EVALUATION_MODEL", "gpt-4o-mini")
ragas_eval_llm = llm_factory(evaluation_model_name)
ragas_answer_accuracy_evaluator = AnswerAccuracy(llm=ragas_eval_llm)

def answer_accuracy_evaluator(input, output, reference):
    # In the context of an evaluator, input still refers to the input field
    # defined on the datsaset. Reference refers to the datasets 
    # output/expected/reference field. Output is the value returned by the 
    # task function.
    sample = SingleTurnSample(
        user_input=list(input.values())[0],
        response=output,
        reference=list(reference.values())[0]
    )
    return ragas_answer_accuracy_evaluator.single_turn_score(
        sample
    )