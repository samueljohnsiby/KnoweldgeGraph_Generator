# main.py (or any Python script)

import os
from dotenv import load_dotenv

# Load variables from .env into the environment
load_dotenv()

# Access configuration variables
api_key = os.environ.get("API_KEY")

# Use the configuration variables
print(f"API Key: {api_key}")

