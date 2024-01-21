import requests
from bs4 import BeautifulSoup
import json

def save_to_json(dati, filename):
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(dati, json_file, ensure_ascii=False, indent=2)

def count_models(dati):
    model_counts = {}

    for auto_info in dati:
        marka_modelis = auto_info["marka_modelis"]
        if marka_modelis in model_counts:
            model_counts[marka_modelis] = model_counts[marka_modelis] + 1
        else:
            model_counts[marka_modelis] = 1

    return model_counts

def iegut_auto_datus(razotajs):
    dati = []

    lapas_numurs = 1
    
    if razotajs:
        while True: 
            URL = f"https://www.ss.lv/lv/transport/cars/{razotajs}/photo/page{lapas_numurs}.html"
            response = requests.get(URL)
            if response.status_code == 200:
                content = response.text
                soup = BeautifulSoup(content, "html.parser")
                sludinajumi = soup.find_all('td', class_="ads_album_td")

                if sludinajumi:
                    for sludinajums in sludinajumi:
                        if razotajs in sludinajums.find('td', align = "center").get_text().strip():         
                            marka_modelis = sludinajums.find('td', align="center").get_text().strip()
                            
                            autoDati = sludinajums.find_all('td', c="2")
                            izlaiduma_gads = autoDati[0].get_text().strip()
                            tilpums = autoDati[1].get_text().strip()
                            nobraukums = autoDati[2].get_text().strip()

                            auto_info = {
                                "marka_modelis": marka_modelis,
                                "izlaiduma_gads": izlaiduma_gads,
                                "tilpums": tilpums,
                                "nobraukums": nobraukums
                            }

                            dati.append(auto_info)
                            
                    lapas_numurs = lapas_numurs+1
                else:
                    break
            else:
                print("Kļūda ar signālu!")
                exit()
        return dati

    elif not razotajs:
        while True: 
            URL = f"https://www.ss.lv/lv/transport/cars/today-5/photo/page{lapas_numurs}.html"
            response = requests.get(URL)
            if response.status_code == 200:
                content = response.text
                soup = BeautifulSoup(content, "html.parser")
                sludinajumi = soup.find_all('td', class_="ads_album_td")

                if not sludinajumi:
                    break
                
                for sludinajums in sludinajumi:   
                    marka_modelis = sludinajums.find('td', align="center").get_text().strip()

                    autoDati = sludinajums.find_all('td', c="2")
                    izlaiduma_gads = autoDati[0].get_text().strip()
                    tilpums = autoDati[1].get_text().strip()
                    nobraukums = autoDati[2].get_text().strip()

                    auto_info = {
                        "marka_modelis": marka_modelis,
                        "izlaiduma_gads": izlaiduma_gads,
                        "tilpums": tilpums,
                        "nobraukums": nobraukums
                    }

                    dati.append(auto_info)
                        
                lapas_numurs = lapas_numurs+1
            else:
                print("Kļūda ar signālu!")
                exit()
        return dati


razotajs = input("Ievadiet interesējošās markas nosaukumu (piemēram, BMW, Audi utt.): ").strip()
if razotajs:
    razotajs = razotajs.title()

dati = iegut_auto_datus(razotajs)

if razotajs:
    if len(dati) != 0:
        save_to_json(sorted(dati,key=lambda x: x["marka_modelis"]), f"{razotajs}.json")
        print(f"Dati saglabāti failā {razotajs}.json")
    else:
        print("Notikusi kļūda, varbūt jūs ievadijāt marku, kas nav ss.com")
        exit()
elif not razotajs:
    save_to_json(sorted(dati,key=lambda x: x["marka_modelis"]), "visas_masinas.json")
    print("Dati saglabāti failā visas_masinas.json")

model_counts = count_models(dati)
for marka_modelis, skaits in model_counts.items():
    print(f"{marka_modelis}: {skaits}")
