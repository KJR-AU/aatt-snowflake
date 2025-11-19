import os
import pandas as pd
import streamlit as st
from snowflake.connector import connect
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Age COE Dashboard", layout="wide")

def get_conn():
    return connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        role=os.environ["SNOWFLAKE_ROLE"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ["SNOWFLAKE_SCHEMA"],
    )

@st.cache_data(ttl=300)
def run_query(sql):
    with get_conn() as con:
        cur = con.cursor()
        try:
            cur.execute(sql)
            cols = [c[0] for c in cur.description]
            rows = cur.fetchall()
            return pd.DataFrame(rows, columns=cols)
        finally:
            cur.close()

st.title("Age COE Metrics")

col1, col2 = st.columns(2)

with col1:
    st.header("Estimation — MAE")
    df_mae = run_query("select * from METRICS_ESTIMATION order by slice_type, gate")
    st.dataframe(df_mae)
    if not df_mae.empty:
        overall = df_mae[df_mae["SLICE_TYPE"]=="overall"][["SAMPLES","MAE_YEARS","SD_YEARS"]]
        st.subheader("Overall")
        st.table(overall)

with col2:
    st.header("Age-gate Metrics")
    df_gate = run_query("select * from METRICS_GATES order by gate")
    st.dataframe(df_gate)

st.header("Verification Time by Method")
df_time = run_query("select * from METRICS_VERIFICATION_TIME order by method")
st.dataframe(df_time)
