import requests

from environment_variables import api_key


def get_last_album_cover(username: str):
    url = "https://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "user.getrecenttracks",
        "user": username,
        "api_key": api_key,
        "format": "json",
        "limit": 1,
    }

    response = requests.get(url, params=params)
    data = response.json()

    track = data["recenttracks"]["track"][0]
    images = track.get("image", [])

    for image in reversed(images):
        if image.get("#text"):
            return image["#text"]

    return ""
