# MySQL To Snowflake with DLT
This example demonstrates how to load data into snowflake from a MySQL database 
using Data Load Tool (DLT).

## Instructions
1. Create configuration files

Create a `.env` file to configure the mysql database
```
# Root password for the MySQL server (used only for the root user, avoid using in apps)
MYSQL_ROOT_PASSWORD=supersecretrootpass

# Name of the default database to be created at container startup
MYSQL_DATABASE=dlt_demo

# Application-specific MySQL username (non-root user your app/pipeline will use)
MYSQL_USER=myappuser

# Password for the application-specific user
MYSQL_PASSWORD=supersecretuserpass

# Hostname or IP address where MySQL is running (inside docker-compose this could be 'db'; outside it's usually 'localhost')
MYSQL_HOST=localhost

# Port number MySQL listens on (default is 3306)
MYSQL_PORT=3306
```

Create `.dlt/secrets.toml` and add snowflake credentials

```
[destination.snowflake.credentials]
database = "dlt_demo"
password = "your-password"
username = "LOADER"
host = "LNKLFMM-EO96522"
warehouse = "COMPUTE_WH"
role = "DLT_LOADER_ROLE"
```

Ensure that these entities are created in snowflake

```
-- create database with standard settings
CREATE DATABASE dlt_data;
-- create new user - set your password here
CREATE USER loader WITH PASSWORD='<password>';
-- we assign all permissions to a role
CREATE ROLE DLT_LOADER_ROLE;
GRANT ROLE DLT_LOADER_ROLE TO USER loader;
-- give database access to new role
GRANT USAGE ON DATABASE dlt_data TO DLT_LOADER_ROLE;
-- allow `dlt` to create new schemas
GRANT CREATE SCHEMA ON DATABASE dlt_data TO ROLE DLT_LOADER_ROLE;
-- allow access to a warehouse named COMPUTE_WH
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO DLT_LOADER_ROLE;
-- grant access to all future schemas and tables in the database
GRANT ALL PRIVILEGES ON FUTURE SCHEMAS IN DATABASE dlt_data TO DLT_LOADER_ROLE;
GRANT ALL PRIVILEGES ON FUTURE TABLES IN DATABASE dlt_data TO DLT_LOADER_ROLE;
```

2. Initialise the mysql database

`docker compose up -d`

This will expose a mysql database on port `3036` and an admin dashboard on port 
`8080`. A SQL script will be run on initialisation to load data into the
database. The structure of the data can be explored through the admin 
dashboard.

3. Confirm the database setup

Navigate to `0.0.0.0:8080`, in the column on the left you should see a database with the name defined in `MYSQL_DATABASE` in `.env`. The database should contain the tables `customers`, `addresses`, `products` etc.

4. Install dependencies

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
5. Run the pipeline

`python extract.py`