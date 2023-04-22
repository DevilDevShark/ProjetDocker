import sys

import requests

API_URL = "http://api:5001"

try:
    response = requests.get(f"{API_URL}/health")
    if response.status_code != 200:
        sys.exit(1)
except Exception:
    sys.exit(1)

sys.exit(0)
