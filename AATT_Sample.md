# AATT Snowflake Sample
This sample demonstrates a number of features of Snowflake using data obtained in the Australian Age Assurance Technology Trial (AATT). We demonstrate the full data pipeline from ingestion through to analysis of data both graphically and with the use of natural language queries.




## Loading and Ingestion

#### dlt - data load tool
We have utilised the open source tool, dlt, for extraction and load of data from external sources. We have demonstrated loading from an external MySQL database - and would be applicable for loadng from almost any standard database - from Microsoft SQL Server, to PostgreSQL to Oracle. Data can be loaded either in full or incrementally as your data changes.


#### Snowsight
A demonstration of manually loading tabular data (csv) into landing tables.

#### SnowSQL
Use of SnowSQL to load data into Snowflake staged areas

## Transformation

#### dbt
Use of dbt to transform data by cleaning, aggregating and rationaling data in tables/views. We also use dbt's in-built testing facility for data integrity and quality checks.

#### Notebooks
An alternative data cleansing and aggregation approach was carried out using Python and SQL Notebooks. 


## Visualisation
One of the main goals of data transformation is to build views ready for business intelligence (BI). We have used streamlit to help visualise tabular data remotely as well as set up graphical visualisations within the integrated streamlit environment.

#### streamlit
Python-based web front-end tool for easy visualisation of data. We have samples of running remotely (using Snowflake Python Connector) as well as "in-cloud" within the integrated streamlit environment in Snowflake.

#### Graphing Tools
We have used Vega-Altair to carry out declarative graphing of data. Because of the well integrated Python environment it is also easy to use other grpahics libraries such as Matplotlib and Plotly.


## Infrastructure Creation

#### Worksheets
Use of worksheets to construct databases, roles and tables.

#### Terraform
Example Infrastructure as Code (IaC) source to create a similar set up to what can be achived with Worksheets.


## AI
We have tested a number of Snowflake Cortex features around the use of LLMs, RAGs, embeddings and Evals within the Snowflake environment.

#### Retrieval Augmented Generation
A RAG was built to explore the AATT Participant "Practice Statements". These documents describe what each technology provider brings to the table in the Age Assurance space. Natural language queries (based on streamlist_)

#### Langchain integration
