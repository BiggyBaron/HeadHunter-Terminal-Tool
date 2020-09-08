import requests
from pprint import pprint
import datetime
from dateutil.parser import parse


data = requests.get('https://api.hh.ru/areas').json()

def find_city(name):
    cities = requests.get('https://api.hh.ru/areas').json()[2]
    # pprint(cities)
    found = -1
    for c in cities["areas"]:
        if c["name"] == str(name):
            found = c["id"]
    
    if int(found) >= 0:
        return found
    else:
        return None


def all_cities():
    cities = requests.get('https://api.hh.ru/areas').json()[2]
    cits = []
    for c in cities["areas"]:
        cits.append(c["name"])
    
    return cits


def all_pro_types():
    profs = requests.get('https://api.hh.ru/specializations').json()
    # pprint(profs)
    types = []
    for p in profs:
        types.append(p["name"])
    return types


def all_profs_in_type(type):
    profs = requests.get('https://api.hh.ru/specializations').json()
    pros = []
    for p1 in profs:
        if p1["name"] == str(type):
            for p in p1["specializations"]:
                pros.append([p["name"], p["id"]])
    return pros


def find_jobs(city, type):
    req = "https://api.hh.ru/vacancies?area=X&specialization=Y"
    places = requests.get(req.replace("X", city).replace("Y", type)).json()
    ps = []
    for p in places["items"]:
        ps.append({
            "name": p["name"],
            "boss": p["employer"]["name"],
            "boss_url": p["employer"]["url"],
            "salary": p["salary"],
            "url": p["url"],
            "date": parse(p["published_at"])
        })
    return ps


def generate_texts(jobs):
    texts = []
    for j in jobs:
        text = "Требуется: [" + str(j["name"]) + "](" + str(j["url"]) + ")\n"
        text += "Компания: [" + str(j["boss"]) + "](" + str(j["boss_url"]) + ")\n"
        if j["salary"] == None:
            j["salary"] = "Без ЗП"
        else:
            j["salary"] = "От " + str(j["salary"]["from"]) + " до " + str(j["salary"]["to"]) + " в " + str(j["salary"]["currency"]) + "\n"
        text += "ЗП: " + str(j["salary"]) + "\n"
        texts.append(text)
    return texts

print("Все города: ")
print(all_cities())
city = find_city(input("Введите имя города: "))
print()
print()
print("Все виды специализаций: ")
print(all_pro_types())
type_is = input("Введите имя специализации: ")
print()
print()
print("Все виды специальностей в группе: ")
print(all_profs_in_type(type_is))
code_type = input("Введите код специализации: ")
print()
print()
print("Ваши вакансии: ")
for g in generate_texts(find_jobs(city, code_type)):
    print(g)

