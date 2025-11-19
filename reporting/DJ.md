# DJ's work

DJ has create a dbt proejct to transform raw AATT data into a cleansed form, and also a streamlit app to display some tables of data.


## DBT

### Source Table
Data is loaded from a raw set of aatt data as found in the `aatt-results` channel from the AATT project. The data has 3 files, and this project uses the one called `results.csv`. This is actually a joined version of a number of tables within the PostgreSQL database that was used by the AATT framework.

DJ has instructions in his README as to how that file should be loaded.

### Staging Layer (Views)
* `STG_RESULTS` cleans and transforms RAW_RESULTS
* Normalisation - eg AE --> Estimation
* Calculates subject age in years
* Converts verification status to boolean
* Parses verification time into seconds
* Applies data quality constraints

### Intermdiate Layer
`INT_ABS_ERROR` is a table that:
  * Calulates absolute error for methods
  * Computes statistical trimming (ie remove outliers beyond 2 std devs)
  * Provides mean and std deviantion of abs errors by method
  * 



## Streamit
