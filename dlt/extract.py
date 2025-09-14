import dlt
from dlt.sources.sql_database import sql_database
import os
from dotenv import load_dotenv

load_dotenv()

# --- Configure pipeline ---
pipeline = dlt.pipeline(
    pipeline_name="mysql_to_snowflake",
    destination="snowflake",
    dataset_name="mysql_replica",  # maps to schema in Snowflake
)

# --- MySQL source ---
# Select which tables to replicate
tables = ["customers", "products", "orders", "order_items", "payments", "events"]

source = sql_database(
    credentials={
        "drivername": "mysql+pymysql",
        "username": "root",
        "password": os.getenv("MYSQL_ROOT_PASSWORD"),
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "database": os.getenv("MYSQL_DATABASE"),
    },
    schema=os.getenv("MYSQL_DATABASE"),
    # replicate only specific tables
    table_names=tables,
)

# --- Run the pipeline ---
if __name__ == "__main__":
    info = pipeline.run(source)
    print(info)
