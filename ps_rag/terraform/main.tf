# Warehouse
resource "snowflake_warehouse" "learning_wh" {
  name                = var.snowflake_warehouse
  warehouse_size      = "XSMALL"
  auto_suspend        = 300
  auto_resume         = true
  initially_suspended = true
  comment             = "Learning / demo warehouse provisioned by Terraform"
}

# Database
resource "snowflake_database" "rag_db" {
  name        = var.snowflake_database
  comment     = "RAG demo database provisioned by Terraform"
  data_retention_time_in_days = 1
}

# Schema
resource "snowflake_schema" "public_schema" {
  database = snowflake_database.rag_db.name
  name     = var.snowflake_schema
  comment  = "PUBLIC schema for RAG demo"
}

# Stages
resource "snowflake_stage" "pdf_stage" {
  name      = "PDF"
  database  = snowflake_database.rag_db.name
  schema    = snowflake_schema.public_schema.name
  comment   = "Stage for PDF files"
}

resource "snowflake_stage" "docx_stage" {
  name      = "DOCX"
  database  = snowflake_database.rag_db.name
  schema    = snowflake_schema.public_schema.name
  comment   = "Stage for DOCX files"
}


#################################
# Create custom role: PS_RAG_ROLE
#################################
resource "snowflake_account_role" "ps_rag_role" {
  name    = var.snowflake_role_name
  comment = "Role for AATT Practice Statements RAG application"
}

# Grant this role to SYSADMIN (or whichever role should inherit it)
resource "snowflake_grant_account_role" "grant_ps_rag_to_accountadmin" {
  role_name        = snowflake_account_role.ps_rag_role.name
  parent_role_name = "ACCOUNTADMIN"
}

#################################
# Grants: allow PS_RAG_ROLE usage
#################################

# Grant warehouse usage
resource "snowflake_grant_privileges_to_account_role" "wh_usage_to_ps_rag" {
  account_role_name = snowflake_account_role.ps_rag_role.name
  privileges        = ["USAGE"]
  on_account_object {
    object_type = "WAREHOUSE"
    object_name = snowflake_warehouse.learning_wh.name
  }
}

# Grant database usage (so the role can see the database)
resource "snowflake_grant_privileges_to_account_role" "db_usage_to_ps_rag" {
  account_role_name = snowflake_account_role.ps_rag_role.name
  privileges        = ["USAGE"]
  on_account_object {
    object_type = "DATABASE"
    object_name = snowflake_database.rag_db.name
  }
}