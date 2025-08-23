import requests


def get_token(api_key: str) -> dict:
    url = "https://ws.audioscrobbler.com/2.0/"
    params = {"method": "auth.gettoken", "api_key": api_key, "format": "json"}

    response = requests.get(url, params=params)
    return response.json()
