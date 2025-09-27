import requests
import json

with open("assets/heroes.json", "w") as f:
    heroes = requests.get("https://assets.deadlock-api.com/v2/heroes").json()
    json.dump(heroes, f)

with open("assets/items.json", "w") as f:
    items = requests.get("https://assets.deadlock-api.com/v2/items").json()
    json.dump(items, f)
