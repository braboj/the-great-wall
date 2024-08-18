import requests

# Endpoint URL
url = 'http://127.0.0.1:8080/profiles/config/'

# Query parameters
params = {'num_teams'}

# Send a GET request
response = requests.get(url)

# Check the response
if response.status_code == 200:
    print("Response from server:", response.json())

else:
    print("Error:", response.status_code)
