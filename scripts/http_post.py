import requests

# data = {
#     "volume_ice_per_foot": 195,
#     "cost_per_volume": 1900,
#     "target_height": 30,
#     "max_section_count": 2000,
#     "build_rate": 1,
#     "num_teams": 20,
#     "cpu_worktime": 0.01,
#     "profile_list": [[21, 25, 28], [17], [17, 22, 17, 19, 17]]
# }

# Endpoint URL
url = 'http://127.0.0.1:8000/profiles/config/'

# Sample data
data = {
    'num_teams': 20,
    'profiles': [[1, 1, 1], [1], [1, 1, 1, 1, 1]]
}

# Send a POST request
response = requests.post(url, json=data)

# Check the response
if response.status_code == 200:
    print("Response from server:", response.json())
else:
    print("Error:", response.status_code)
