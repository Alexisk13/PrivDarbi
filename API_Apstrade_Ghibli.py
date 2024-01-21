import json
import requests

# 1. uzdevums
response_films = requests.get("https://ghibliapi.dev/films")
data_list = response_films.json()

number_of_items = len(data_list)
for i in range(number_of_items):
    filmas_nos = data_list[i]['title']
    filmas_apr = data_list[i]['description']
    filmas_rez = data_list[i]['director']
    filmas_IzlDat = data_list[i]['release_date']
    print(f'{i+1}: "{filmas_nos}" \n*{filmas_apr}* \n-{filmas_rez} \n-{filmas_IzlDat}')
    print()

# 2. uzdevums  

def main():
    url = "https://ghibliapi.dev/locations"
    response = requests.get(url)

    if response.status_code == 200:
        locations = response.json()
        cleaned_data = [clean_location_data(location) for location in locations]
        save_to_json(cleaned_data, "locations_ghibli.json")
        print("Data saved to locations.json")
    else:
        print("Failed to retrieve data from the API")

def clean_location_data(location):
    return {
        "Nosaukums": location.get("name", ""),
        "Klimats": location.get("climate", ""),
        "Reljefs": location.get("terrain", ""),
        "Iemītnieki": [clean_resident_data(get_resident_data(resident_url)) for resident_url in location.get("residents", [])],
    }

def clean_resident_data(resident_data):
    return {
        "id": resident_data.get("id", ""),
        "Nosaukums": resident_data.get("name", ""),
        "Dzimums": resident_data.get("gender", ""),
        "gadi": resident_data.get("age", ""),
        "Acu_krāsa": resident_data.get("eye_color", ""),
        "Matu_krāsa": resident_data.get("hair_color", ""),
        "Filmas": [get_film_name(film_url) for film_url in resident_data.get("films", [])],
        "Iemītnieki": get_species_name(resident_data.get("species", ""))
    }

def get_resident_data(resident_url):
    if "TODO" in resident_url:
        return {}  
    if resident_url:  
        response = requests.get(resident_url)
        if response.status_code == 200:
            return response.json()
    return {}  

def get_film_name(film_url):
    if "TODO" in film_url:
        return ""  
    if film_url:  
        response = requests.get(film_url)
        if response.status_code == 200:
            return response.json().get("title", "")
    return ""  

def get_species_name(species_url):
    if "TODO" in species_url:
        return ""  
    if species_url:  
        response = requests.get(species_url)
        if response.status_code == 200:
            return response.json().get("name", "")
    return ""  

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()