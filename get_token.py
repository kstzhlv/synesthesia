import requests

url = "https://ws.audioscrobbler.com/2.0/"
params = {"method": "auth.gettoken", "api_key": "YOUR_API_KEY", "format": "json"}

response = requests.get(url, params=params)
data = response.json()

print(data)
