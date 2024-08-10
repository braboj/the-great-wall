import requests

# Endpoint URL
url = 'http://127.0.0.1:8000/profiles/config/'

# Sample data
data = {'num_teams': 1}

# Send a POST request
response = requests.post(url, json=data)

# Check the response
if response.status_code == 200:
    print("Response from server:", response.json())
else:
    print("Error:", response.status_code)


# Endpoint URL
url = 'http://127.0.0.1:8000/profiles/config/'

# Query parameters
params = {'num_teams'}

# Send a GET request
response = requests.get(url, params=params)

# Check the response
if response.status_code == 200:
    print("Response from server:", response.json())

else:
    print("Error:", response.status_code)
