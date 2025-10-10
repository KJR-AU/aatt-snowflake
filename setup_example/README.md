## Setup Example
This sub-folder contains a sample worksheet that can be copied into a new worksheet in Snowflake to create a test AATT database.

It does the following:

```
    NOTE: Ensur you are in the SYSADMIN role to be able to create the database and the role
```

### Create Database
* Create a database called `AATT_SNOWFLAKE_DEMO_DB`
  
### Create Role and Grant Permissions
* Create a role called `AATT_ROLE`
* Grant specific users to that role
* Allow at least the following operations using the role:
  * usage on AATT_SNOWFLAKE_DEMO_DB database
  * usage on `public` schema of above db
  * select on all tables within that schema
  * allow create table on the schema
  * allow create view on the schema
  * allow create stage on the schema
  * allow create file format on the schema
  * select on future tables

### Create a Stage and Upload the csv file
* Creates a stage to load the csv data
* Put the file into the stage (compress using gzip)

```
    NOTE: this must be done using `snowsql`. The snowflake environment does not have access to the local PC filesystem
```

### Load the file into a Landing Table
* Create a fileformat




a workspace 