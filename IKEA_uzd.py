import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.ikea.lv/lv/rooms/edamistaba/edamgaldi"
response = requests.get(URL)
content = response.text

soup = BeautifulSoup(content, "lxml")

box = soup.find('div', class_="container presentationContainer")
cardBodies = box.find_all('div', class_="card-body")

produkti = []

for cardBody in cardBodies:
    Nosaukums = cardBody.find("h3").get_text().strip()
    Apraksts = cardBody.find("h4").get_text().strip()
    Cena = cardBody.find('div', class_="itemPrice-wrapper").get_text().strip()

    produkts_info = {
        "Nosaukums": Nosaukums,
        "Apraksts": Apraksts,
        "Cena": Cena
    }

    produkti.append(produkts_info)

    print(f"{Nosaukums}: {Cena}")

with open("produkti.json", "w", encoding="utf-8") as json_file:
    json.dump(produkti, json_file, ensure_ascii=False, indent=2)
