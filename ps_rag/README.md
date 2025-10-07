# AATT Practice Statement RAG
This project deploys sets up a simple RAG chatbot to answer questions about
practice statements from the AATT project. A vector database is created and
populated on Snowflake and a langchain client is provided. Additionally, an
agent is created in Snowflake's Cortex service and a client provided to
interact with it.

## Load documents
The documents are a collection of PDF and DOCX files containing practice
statements submitted to the AATT project. These practice statements outline
how products offered by age-assurance technology providers are built and 
operate. 

The documents were accessed from a [ZIP file hosted on Sharepoint](https://kjra.sharepoint.com/:f:/r/clients/Shared%20Documents/AATT/Snowflake-Demo?csf=1&web=1&e=eDifQ7).

Once downloaded and extracted, a script can be run to upload the relevant 
documents to a snowflake stage. 





PDF and DOCX files were extracted from `Practice Statement` subdirectories (e.g. `AE/Practice Statements`), product type (AE, AI etc) prepended to filenames collated in another directory.

The 
