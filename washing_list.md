# Concepts in Snowflake

## List of features of Snowflake


## What featues our demonstration shows
- dlt
  - an example loading from a MySQL database
- dbt
  - T in ELT
  - Can run within embedded Snowflake environment
  - Tests to ensure data integrity, uniqueness and non-null checks
- streamlit
  - Simple Python user interface
  - can be run directly inside an embedded sub-system of Snowflake
- Vega-Altair
  - Declarative graphing
- Cortex
  - AI library in Snowflake
- RAG
- Embeddings
- Evals
  - eg TrueLens
- Interfaces used
  - Snowsight - web interface
  - SnowSQL - cli for running SQL
  - Snowpark - dataframe coding similar to pandas
    - runs inside snowflake
  - Snowflake Notebooks
    - Jupyter notebooks in Snowflake
  - Snowflake Worksheets
  - snow - Snowflake CLI
  - streamlit
  - Python Connector
- Use of stages
- 

## Other features available
  - REST APIs
  - 


## QA Focus
 - Testing LLM results with evals
 - Safe and secure data-sharing

 - Designing robust ELT pipelines with data validation at each stage
   - eg Use dbt to transform from raw data to staged cleansed data to modelled analytics
 - Implementing automated data quality and regression testing
   - eg Use of dbt tests to verify key metrics are reasonable, data holds inetegrity
 - Building Observability Frameworks
   - Querying logs to monitor data freshness and failure rates
   - Creation of Monitoring Dashboards using streamlit/Power BI 
   - Raising of alerts
 - Governence advice
   - Securing data via definition of role-based access
   - Environment separation
   - Naming and versioning standards
 - LLM Evaluation and Quality Assurance
   - Model Accuracy and Consistency Training
     - Structured test suites for prompts and expected outputs
     - Regression testing by way of measuring factual correctness, coherence and consistency
   - Compliance Evaluation
     - Run controlled tests to detect policy violations, unfair responses or sensitive content
     - Report and track in Issue systems such as JIRA
   - Evaluation Framnework Development
     - Implement automated eval pipelines using tools such as langchain and TrueLens
   - Benchmarking and Model Comparison
     - Comparison of multiple LLMs (eg Cluade, GPT, LLama)
     - Production of objective reports to guide model selection and fine-tuning strategy
- 

