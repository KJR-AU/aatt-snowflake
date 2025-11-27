from phoenix.client import Client
import os

BASE_URL = os.getenv("PHOENIX_BASE_URL", "http://localhost:30651")
API_KEY = os.getenv("PHOENIX_API_KEY")

client = Client(base_url=BASE_URL, api_key=API_KEY)