import streamlit as st
import altair as alt
from snowflake.snowpark.context import get_active_session

session = get_active_session()

query = "SELECT NAME, PROVIDER_COUNT FROM AATT_SNOWFLAKE_DEMO_DB.PUBLIC.PROVIDER_COUNTS"
df = session.sql(query).to_pandas()

df["PERCENT"] = df["PROVIDER_COUNT"] / df["PROVIDER_COUNT"].sum() * 100

st.title("Results by Provider")
st.markdown(
    """
    _This chart shows the distribution of results by provider._
    """
)

chart = (
    alt.Chart(df)
    .mark_arc(innerRadius=50)
    .encode(
        theta=alt.Theta(field="PROVIDER_COUNT", type="quantitative", title="Count"),
        color=alt.Color(
            field="NAME",
            type="nominal",
            scale=alt.Scale(scheme="tableau10"),
            legend=alt.Legend(title="Provider"),
        ),
        tooltip=[
            alt.Tooltip("NAME", title="Provider"),
            alt.Tooltip("PROVIDER_COUNT", title="Count"),
            alt.Tooltip("PERCENT", title="Percent", format=".1f"),
        ],
    )
)

st.altair_chart(chart, use_container_width=True)

# --- Data table below chart ---
st.subheader("Provider Counts Table")
st.dataframe(
    df.sort_values("PROVIDER_COUNT", ascending=False),
    use_container_width=True,
    hide_index=True
)
