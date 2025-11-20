import pandas as pd

experiment_name: str = "nifty_mccarthy"
df = pd.read_csv(f"experiments/{experiment_name}.csv")

print(df.head()["error"][0])