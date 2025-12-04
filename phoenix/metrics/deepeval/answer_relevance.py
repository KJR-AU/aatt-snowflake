from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
import os

evaluation_model_name: str = os.getenv("EVALUATION_MODEL", "gpt-4o-mini")

def answer_relevance_evaluator(input, output):
    metric = AnswerRelevancyMetric(
        threshold=0.7,
        model=evaluation_model_name,
        include_reason=True
    )
    test_case = LLMTestCase(
        input=list(input.values())[0],
        actual_output=output
    )
    metric.measure(test_case)
    return metric.score, metric.reason