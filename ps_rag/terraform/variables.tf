
variable "snowflake_warehouse" { 
    type = string  
    default = "PS_RAG_WH" 
}
variable "snowflake_database"  { 
    type = string  
    default = "AATT_PS_RAG" 
}
variable "snowflake_schema"    { 
    type = string  
    default = "PUBLIC"
}

variable "snowflake_role_name" {
    type = string
    default = "AATT_PS_RAG_ROLE"
}
