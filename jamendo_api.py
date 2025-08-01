import requests
from config import JAMENDO_CLIENT_ID

API_URL = "https://api.jamendo.com/v3.0/tracks/"


def search_music(query, limit=5):
    params = {
        "client_id": JAMENDO_CLIENT_ID,
        "format": "json",
        "limit": limit,
        "fuzzytags": query,
        "include": "musicinfo",
        "audioformat": "mp31"
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    if "results" not in data or not data["results"]:
        return []

    results = []
    for track in data["results"]:
        results.append({
            "id": track["id"],
            "name": track["name"],
            "artist": track["artist_name"],
            "audio": track["audio"]
        })
    return results


def download_music_file(url, filename="downloaded_track.mp3"):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)
    return filename
