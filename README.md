# AATT Snowflake Demo
This repo captures manifests of putting together a copy of the AATT project inside a Snowflake environment to try to use Snowflake's secure cloud-based infrastrcuture to import, house and provide a nbasis for domain-based analysis.


## What is AATT
AATT stands for Age Assurance Technology Trial which was a trial initiated by the Australian government in late 2024 to evaluate the technologies availabl for electronically determining a person's age. Specifically, it was a precursor to making it law for content providers (such as social media platforms) to ensure that a young person was old enough to participate in and ingest that provider's content.

## Why use AATT
The AATT project captured a number of individual tests where each test had:

 * a subject (ie an individual)
 * a provider (ie the software under test)
 * the subjects actual age
 * an "age-gate" in operation
 * a method used (verification/estimation/inference)
 * either
   * an estimated/verified age
   * an under/over result


## AATT reporting
A report was put together based on these results, where evidence from testing was to be provided. The report made use of the result data, as well as "Practice Statements" which were "declarations" by participants on what their software could do.


## Snowflake Areas and Topics
The following high-level areas and concepts were investigated and/or demonstrated as part of the AATT Snowflake Demo:

* dlt
* dbt
* SnowPark API
* SnowSQL
* Notebooks
* Worksheets
* Databases
* Stages
* streamlit
* Altair Vega
* Cortex
* RAG

Focus on Testing
* Evals
* dbt tests


## DLT
Data Load Tool. This is similar to DBT which handles the "transform" component of ELT (Extract/Load/Transform), but DLT handles the "load" component.

