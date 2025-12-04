from deepeval.metrics import PIILeakageMetric
from deepeval.test_case import LLMTestCase
import os

evaluation_model_name: str = os.getenv("EVALUATION_MODEL", "gpt-4o-mini")

def pii_leakage_evaluator(input, output):
    """Binary PII detector.

    Returns one if free of PII, else zero.
    """
    metric = PIILeakageMetric(
        model=evaluation_model_name,
        include_reason=False,
        strict_mode=True
    )
    test_case = LLMTestCase(
        input=list(input.values())[0],
        actual_output=output
    )
    metric.measure(test_case)
    return metric.score