import streamlit as st
import pandas as pd
import ast
from pathlib import Path

# -----------------------------------------------------
# 🧱 Helper functions
# -----------------------------------------------------
def load_experiments(directory: str = "experiments") -> dict[str, pd.DataFrame]:
    """
    Load all CSVs from the experiments directory and return a dict of DataFrames keyed by experiment name.
    """
    base = Path(directory)
    csv_files = list(base.glob("*.csv"))
    experiments = {}

    if not csv_files:
        st.warning(f"No CSV files found in '{directory}'")
        return experiments

    for f in csv_files:
        try:
            df = pd.read_csv(f)
            if not df.empty and "experiment_name" in df.columns:
                experiment_name = str(df.iloc[0]["experiment_name"])
                df["source_file"] = f.name
                experiments[experiment_name] = df
            else:
                st.warning(f"⚠️ Skipping {f.name} (no experiment_name column or empty)")
        except Exception as e:
            st.error(f"❌ Error loading {f.name}: {e}")

    return experiments


# -----------------------------------------------------
# 🎨 Streamlit UI
# -----------------------------------------------------
st.set_page_config(page_title="RAGAS Experiment Browser", layout="wide")
st.title("🧪 RAGAS Experiment Results Browser")

# Load all experiments
experiments = load_experiments("experiments")

if not experiments:
    st.stop()

# -----------------------------------------------------
# 📋 Primary View — Experiment List
# -----------------------------------------------------
st.sidebar.header("🔍 Select Experiment")
experiment_names = sorted(list(experiments.keys()))

selected_experiment = st.sidebar.selectbox(
    "Choose an experiment to explore", experiment_names
)

# -----------------------------------------------------
# 📊 Detail View — Selected Experiment
# -----------------------------------------------------
if selected_experiment:
    st.subheader(f"📄 Experiment: {selected_experiment}")

    filtered_df = experiments[selected_experiment]
    if not filtered_df.empty:
        source_file = filtered_df["source_file"][0]
        st.subheader(f"Configuration:")

        configuration = {
            "configuration": ["model_name", "temperature", "prompt", "dataset"],
            "value": [filtered_df["model_name"][0], filtered_df["temperature"][0], filtered_df["prompt"][0], filtered_df["dataset_name"][0]]
        }
        configuration_df = pd.DataFrame(configuration)
        mk_df = configuration_df.to_markdown()
        st.markdown(mk_df)

    # --- Summary ---
    st.markdown(f"### Results Overview ({len(filtered_df)} rows)")
    display_cols = [
        "timestamp",
        "user_input",
        "error",
    ]
    # Include metrics if present
    metric_cols = [col for col in filtered_df.columns if col not in display_cols and col.startswith(("metric_"))]
    display_cols.extend(metric_cols)

    st.dataframe(
        filtered_df[display_cols].sort_values("timestamp", ascending=False),
        use_container_width=True,
    )

    # --- Detailed View ---
    st.divider()
    st.markdown("### 🔎 Detailed Record Viewer")

    if not filtered_df.empty:
        idx = st.selectbox(
            "Select a record",
            range(len(filtered_df)),
            format_func=lambda i: filtered_df.iloc[i]["user_input"][:80],
        )
        row = filtered_df.iloc[idx]
        metric_column_names = [v for v in row.index if v.startswith("metric_")]
        metric_values = [row[column_name] for column_name in metric_column_names]

        metrics_df = pd.DataFrame({"name": [name[len("metric_"):] for name in metric_column_names], "value": metric_values})

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 💬 User Input")
            st.info(row["user_input"])

            st.markdown("#### 🤖 Model Response")
            st.write(row["response"])

            st.markdown("#### Metrics")
            st.markdown(metrics_df.to_markdown())

            if pd.notna(row.get("error")) and str(row["error"]).strip():
                st.markdown("#### ⚠️ Error")
                st.error(row["error"])

        with col2:
            st.markdown("#### 📚 Reference Contexts")
            st.write(row["reference_contexts"])

            st.markdown("#### 🎯 Reference Answer")
            st.success(row["reference"])

            st.markdown("#### 🧩 Metadata")
            st.json(
                {
                    "synthesizer_name": row.get("synthesizer_name"),
                    "model_name": row.get("model_name"),
                    "temperature": row.get("temperature"),
                    "prompt": row.get("prompt"),
                    "timestamp": row.get("timestamp"),
                    "source_file": row.get("source_file"),
                }
            )

            if "parsed_metrics" in row and row["parsed_metrics"]:
                st.markdown("#### 📏 Metrics")
                st.json(row["parsed_metrics"])
