import pandas as pd
import json
from cohere_classifier import *

if __name__ == "__main__":
    with open("../api-keys.json", "r") as f:
        api_keys = json.load(f)
        print(f"Found keys for {', '.join(api_keys.keys())}")