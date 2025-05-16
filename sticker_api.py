import requests
sticker_key = "pM64EjTBP7QogQJO0G9XLQwSr6RkAJHj"

def get_sticker(query):
    url = f"https://api.giphy.com/v1/stickers/search"
    params = {
        "api_key": sticker_key,
        "q": query,
        "limit": 10,
        "rating":"g",
        "lang":"en"
    }

    response = requests.get(url, params=params)
    data = response.json()
    results = []

    for item in data.get("data", []):
        gif_url = item["images"]["downsized"]["url"]
        results.append(gif_url)

    return results

