import requests
import json
from concurrent.futures import ThreadPoolExecutor

# 1a.)
root_url = "https://www.swapi.tech/api"

response = requests.get(root_url)
resources = response.json()

films_url = "https://www.swapi.tech/api/films/"

response_films = requests.get(films_url)
films_data = response_films.json()["result"]

with open("star_wars_filmas.json", "w") as json_file:
    json.dump(films_data, json_file, indent=2)

films_dict = {}
for film in films_data:
    film_title = film["properties"]["title"]
    release_date = film["properties"]["release_date"]
    films_dict[film_title] = release_date

for title, date in films_dict.items():
    print(f"Nosaukums: {title}, Izlaišanas datums: {date}")

# 1b.) 
all_characters_data = []

def fetch_character_data(character_url):
    response_character = requests.get(character_url)
    character_data = response_character.json()["result"]
    all_characters_data.append(character_data)

with ThreadPoolExecutor(max_workers=5) as executor:
    for film in films_data:
        characters_url_list = film["properties"]["characters"]
        executor.map(fetch_character_data, characters_url_list)

with open("all_characters.json", "w") as characters_file:
    json.dump(all_characters_data, characters_file, indent=2)

print("Izveidots fails ar visu varoņu informāciju: all_characters.json")

# 1c.)
characters_in_all_films = {}

key_characters = ["C-3PO", "R2-D2", "Chewbacca", "Obi-Wan Kenobi", "Yoda", "Palpatine"]

for character_data in all_characters_data:
    character_name = character_data["properties"]["name"]
    character_gender = character_data["properties"]["gender"]

    if character_name in key_characters:
        characters_in_all_films[character_name] = {"gender": character_gender}
        print(f"Vārds: {character_name}, Dzimums: {character_gender}")

with open("characters_in_all_films.json", "w") as characters_file:
    json.dump(characters_in_all_films, characters_file, indent=2)

print("Izveidots fails ar vārdiem un dzimumiem visiem varoņiem, kas piedalās visās filmās: characters_in_all_films.json")