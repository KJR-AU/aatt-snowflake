# Register UDTF for data flow from Snowflake Internal Stage to Vector Database
from snowflake.snowpark.types import StringType, StructField, StructType
from snowflake.snowpark.functions import udtf
from langchain.text_splitter import RecursiveCharacterTextSplitter
from snowflake.snowpark.files import SnowflakeFile
import PyPDF2, io
import pandas as pd
from session import session
from dotenv import load_dotenv
import os

load_dotenv()

# @udtf(session=session,
#       output_schema=StructType([StructField("chunk", StringType())]),
#       input_types=[StringType()],
#       name=os.environ.get("SNOWFLAKE_EXTRACT_FUNCTION_NAME", "PDF_TEXT_CHUNKER"),
#       is_permanent=True,
#       stage_location="@pdf",
#       replace=True,
#       packages=["langchain==0.3.25", 
#                 "PyPDF2==3.0.1", 
#                 "snowflake-snowpark-python==1.38.0",]
#       )
# class pdf_text_chunker:

#     def read_pdf(self, file_url):
    
#         with SnowflakeFile.open(file_url, 'rb') as f:
#             buffer = io.BytesIO(f.readall())
            
#         reader = PyPDF2.PdfReader(buffer)   
#         text = ""
#         for page in reader.pages:
#             text += page.extract_text()
#         return text

#     def process(self, file_url):

#         text = self.read_pdf(file_url)
        
#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size = 4000, 
#             chunk_overlap  = 400, 
#             length_function = len
#         )
    
#         chunks = text_splitter.split_text(text)
#         df = pd.DataFrame(chunks, columns=['chunks'])
#         yield from df.itertuples(index=False, name=None)


def create_vector_db_table(database: str, schema: str, table: str, function: str):
    query = f'''
    CREATE OR REPLACE TABLE {database}.{schema}.{table} AS 
    SELECT t.$1 AS file_path, c.chunk, SNOWFLAKE.CORTEX.EMBED_TEXT_768('e5-base-v2', c.chunk) as chunk_vec
    FROM (
        SELECT distinct METADATA$FILENAME as file_name
        FROM @{database}.{schema}.PDF t
    ) t,
    LATERAL {database}.{schema}.{function}(build_scoped_file_url(@"{database}"."{schema}"."PDF", t.$1)) c;
    '''
    print(query)
    session.sql(query).collect()

if __name__ == "__main__":
    create_vector_db_table(os.environ.get("SNOWFLAKE_DATABASE"), os.environ.get("SNOWFLAKE_SCHEMA"), "PDF_VECTOR_DB", "PDF_TEXT_CHUNKER")