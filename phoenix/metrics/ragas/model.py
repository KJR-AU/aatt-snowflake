import os
from ragas.llms import llm_factory

evaluation_model_name: str = os.getenv("EVALUATION_MODEL", "gpt-4o-mini")
evaluation_llm = llm_factory(evaluation_model_name)