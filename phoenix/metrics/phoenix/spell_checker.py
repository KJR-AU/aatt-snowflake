from phoenix.evals import ClassificationEvaluator
from phoenix.evals.llm import LLM
import os

evaluation_model_name: str = os.getenv("EVALUATION_MODEL", "gpt-4o-mini")

SCORE_TEMPLATE = """
You are an expert copy editor that checks for grammatical, spelling and typing errors
in a document context. You are going to return a rating for the
document based on the percent of grammatical and typing errors. The score should be
between 1 and 10, where 1 means no words have errors and 10 means all words have errors. 

Example Scoring Rubric
1: no grammatical errors in any word
2: 20% of words have errors
5: 50% of words have errors 
7: 70% of words have errors 
10: all of the words in the context have errors 

#CONTEXT
{context}
#END CONTEXT

#QUESTION
Please rate the percentage of errors in the context on a scale from 1 to 10. 
"""


def spelling_evaluator(output):
    spelling_classifier = ClassificationEvaluator(
        name="spelling",
        prompt_template=SCORE_TEMPLATE,
        llm=LLM(provider="openai", model=evaluation_model_name),
        choices={str(i): i for i in range(1, 11)},
        direction="minimize" # lower scores = better, so direction = minimize 
    )
    if not (result := spelling_classifier.evaluate({"context": output })):
        raise ValueError("No result from spelling evaluator")
    return result[0].score
