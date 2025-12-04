# LLM-as-Judge Relevancy Metric Test Cases (Table Format)

This dataset contains **20 test cases** for evaluating answer relevancy metrics in Retrieval-Augmented Generation (RAG) systems. The cases span:

* **High relevance** (>0.7)
* **Partial relevance** (0.4–0.7)
* **Irrelevant** (<0.25)
* **Distractors** (plausible but wrong)
* **Noisy inputs** (mixed content)
* **Adversarial edge cases** (semantic traps)

Each row lists:

* Input question
* Output summary
* Target score
* Evaluation purpose
* **Pass/Fail expectation** — whether a good relevancy metric *should* rate the answer as relevant enough to pass

---

## **Test Case Table**

| **ID** | **Input Question**                        | **Output Summary**                               | **Target Score** | **Should Pass?** | **Purpose / Evaluation Focus**         |
| ------ | ----------------------------------------- | ------------------------------------------------ | ---------------- | ---------------- | -------------------------------------- |
| **1**  | How does RAG improve factual accuracy?    | Accurate explanation of grounding via retrieval. | **0.90**         | **Yes**          | High-relevance benchmark.              |
| **2**  | Purpose of embeddings in semantic search? | Correct explanation + extra detail.              | **0.80**         | **Yes**          | High relevance with minor drift.       |
| **3**  | Why use vector DBs in RAG?                | Mostly correct, some extra verbosity.            | **0.72**         | **Yes**          | Handles long but relevant answers.     |
| **4**  | How do vector DBs speed search?           | Talks about cheetahs.                            | **0.05**         | **No**           | Detects fully irrelevant content.      |
| **5**  | Role of embeddings in retrieval?          | Talks about SSDs/laptops.                        | **0.15**         | **No**           | Rejects tech-adjacent irrelevance.     |
| **6**  | Why is grounding important in RAG?        | Describes groundwater recharge.                  | **0.20**         | **No**           | Detects misleading lexical overlap.    |
| **7**  | Documents needed for child adoption?      | Talks about pet adoption.                        | **~0.30**        | **No**           | Detects context swap distractors.      |
| **8**  | How does KMS key rotation help security?  | Talks about API key rotation.                    | **~0.35**        | **No**           | Detects concept substitution errors.   |
| **9**  | What determines DNS TTL?                  | CDN caching TTL explanation.                     | **0.40**         | **No**           | Picks up domain confusion.             |
| **10** | Semantic vs keyword search?               | Correct + car trivia noise.                      | **~0.60**        | **Yes**          | Handles mixed relevance + minor noise. |
| **11** | What is RAG used for?                     | Correct + garbled text + parrot fish.            | **~0.55**        | **Yes**          | Noisy + partial corruption robustness. |
| **12** | Why is chunking important for RAG?        | Correct + ISS fan fact.                          | **0.50**         | **Yes**          | Detects partial relevance + drift.     |
| **13** | What is prompt injection?                 | SQL injection explanation.                       | **0.25**         | **No**           | Terminology overlap but wrong domain.  |
| **14** | How does BM25 work?                       | Embedding similarity explanation.                | **0.45**         | **No**           | Incorrect algorithm description.       |
| **15** | Why use hybrid search?                    | Accurate explanation, modern technique.          | **0.88**         | **Yes**          | Strong relevance.                      |
| **16** | What is few-shot prompting?               | Talks about vaccines.                            | **0.10**         | **No**           | Full terminology misclassification.    |
| **17** | How does query rewriting help retrieval?  | Correct + moderate historical noise.             | **0.65**         | **Yes**          | Medium relevance + noise.              |
| **18** | Why is metadata filtering important?      | Accurate, precise explanation.                   | **0.92**         | **Yes**          | High-precision correctness.            |
| **19** | What is embedding dimensionality?         | Talks about image resolution.                    | **0.22**         | **No**           | Numeric terminology confusion.         |
| **20** | How does reranking improve retrieval?     | Correct explanation of cross-encoders.           | **0.81**         | **Yes**          | High relevance with slight expansion.  |

---

## **README / Dataset Overview**

### **Purpose**

This dataset is designed for benchmarking **LLM-as-judge answer relevancy metrics** used to evaluate Retrieval-Augmented Generation (RAG) systems. It helps validate whether models can:

* Reward highly relevant answers
* Penalise irrelevant or misleading ones
* Handle noise, drift, distractors, and hallucinations
* Recognise partial relevance

### **Scoring Ranges Represented**

| Range       | Meaning                                | Examples                      |
| ----------- | -------------------------------------- | ----------------------------- |
| **0.8–1.0** | Very high relevance → should pass      | IDs 1, 2, 15, 18, 20          |
| **0.6–0.8** | Moderate relevance → should pass       | IDs 3, 10, 11, 12, 17         |
| **0.3–0.6** | Partial relevance → mixed expectations | Mainly fail except 10–12      |
| **0.0–0.3** | Low relevance → should fail            | IDs 4, 5, 6, 7, 8, 13, 16, 19 |

### **Pass/Fail Philosophy**

* **Pass** means the answer meets minimum relevance expectations for a RAG system evaluator.
* **Fail** means the answer is sufficiently irrelevant, misleading, or incorrect.

### **Use Cases**

This dataset can be used for:

* Benchmarking evaluator LLMs
* Fine-tuning relevancy scoring models
* Testing RAG retrieval robustness
* Creating evaluation harnesses for QA systems

---

Let me know if you'd like a JSONL export, separate subsets, or additional samples!
