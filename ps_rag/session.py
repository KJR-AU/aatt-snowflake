import os
from snowflake.snowpark import Session
from dotenv import load_dotenv

load_dotenv()

connection_parameters = {
    "user": os.environ["SNOWFLAKE_USER"],
    "password": os.environ["SNOWFLAKE_PASSWORD"],
    "account": f"{os.environ['SNOWFLAKE_ORGANIZATION_NAME']}-{os.environ['SNOWFLAKE_ACCOUNT_NAME']}",
    "warehouse": os.environ.get("SNOWFLAKE_WAREHOUSE"),
    "database": os.environ.get("SNOWFLAKE_DATABASE"),
    "schema": os.environ.get("SNOWFLAKE_SCHEMA"),
    "role": os.environ.get("SNOWFLAKE_ROLE")
}

session = Session.builder.configs(connection_parameters).create()