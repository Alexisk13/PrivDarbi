# Uzdevums 1 
import json

# 1)
print("1)")
data = {"key1" : "valuel", "key2" : "value2"}
json_data = json.dumps(data)
print(json_data)

# 2)
print("2)")
JSON_dotais = """{"key1": true, "key2": false}"""
json_dotais = json.loads(JSON_dotais)
Otras_atslegas_vertiba = json_dotais.get("key2", None)
print("2. atslēgas vērtība:", Otras_atslegas_vertiba)

# 3) 
print("3)")
JSON_dotais = {"key1" : "value2", "key2" : "value2", "key3" : None}
json_data = json.dumps(JSON_dotais, indent=2, separators=(',', '='))
print(json_data)

# 4)
print("4)")
JSON_dotais = {"id" : 1, "name" : "value2", "age" : 29}
sakartots_json = json.dumps(JSON_dotais, separators=(',', ':'), sort_keys=True)
with open('sakartots_dati.json', 'w') as json_faila:
    json_faila.write(sakartots_json)
print("Dati ir saglabāti .json failā un tie ir sakārtoti alfabētiskā secībā.")

# 5)
print("5)")
JSON_dotais = """{
    "company":{
        "employee":{
            "name":"emma",
            "payble":{
                "salary":7000,
                "bonus":800
            }
        } 
    }
}"""
data = json.loads(JSON_dotais)
salary_value = data["company"]["employee"]["payble"]["salary"]
print("Salary vērtība:", salary_value)