import json
from datetime import datetime, timedelta

import requests

base_url = "http://localhost:5001"




# Test creating a new petition
petition_data = {
    "title": "Test Petition",
    "content": "This is a test petition.",
    "end_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S")
}
response = requests.post(f"{base_url}/petitions", json=petition_data)
print(f"Create petition response: {response.status_code}, {response.text}")

# Test getting open petitions
response = requests.get(f"{base_url}/petitions/open")
print(f"Get open petitions response: {response.status_code}, {response.text}")

# Test getting past petitions
response = requests.get(f"{base_url}/petitions/past")
print(f"Get past petitions response: {response.status_code}, {response.text}")

petition_id = 1  
vote_data = {
    "user_id": "test_user",
    "vote_value": True
}
response = requests.post(
    f"{base_url}/petitions/{petition_id}/vote", json=vote_data)
print(f"Vote on petition response: {response.status_code}, {response.text}")
