# run_dbt.py
from dotenv import load_dotenv
import os
import subprocess
import sys

# Path to the dbt project folder (subfolder of current folder)
DBT_PROJECT_DIR = "dbt_project"  # replace with your dbt project folder name

# Load .env from the same folder as this script
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Change working directory to the dbt project
os.chdir(os.path.join(os.path.dirname(__file__), DBT_PROJECT_DIR))

# Get dbt command from CLI, default to "run"
dbt_command = sys.argv[1] if len(sys.argv) > 1 else "run"

# Build the dbt command with any extra args
command = ["dbt", dbt_command] + sys.argv[2:]

# Execute the dbt command
subprocess.run(command)
