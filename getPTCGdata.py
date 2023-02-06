import requests
import time
import random
from bs4 import BeautifulSoup
import re
import json

headers = {
    'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}


def getInfo(url):
    html = requests.get(url, headers=headers)
    soup1 = BeautifulSoup(html.text, 'html.parser')
    st = 0
    evolveMarker = False
    time.sleep(3)
    if soup1.find("span", class_="evolveMarker"):
        evolveMarker = soup1.find("span", class_="evolveMarker").getText()
        evolveMarker = evolveMarker.strip()
        st = len(evolveMarker)

    # 名稱
    name = soup1.find("h1", class_='pageHeader cardDetail').getText()
    name = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]", "", name)[st:]
    # img
    url = soup1.find(class_='cardImage').select_one('img').get("src")

    # HP
    if soup1.find(class_='number'):
        hp = soup1.find(class_='number').getText()

    # 屬性
    if soup1.find(class_='type'):
        pok_type = soup1.find(class_='type').find_next('img').get("src")

    # attr
    attr = soup1.find(class_='commonHeader').getText()
    attr = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]", "", attr)

    # 招式and 特性
    skill_list = {}
    skill_all = soup1.find_all(class_="skill")
    ability = {}

    for sk in skill_all:
        temp = sk.find(class_="skillName").getText()
        if '[特性]' in temp:
            val = sk.find(class_="skillEffect").getText()
            val = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]", "", val)

            ability[temp.replace("[特性]", "")] = val
        else:
            if '規則' in temp:
                continue
            val = sk.find(class_="skillEffect").getText()
            val = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]", "", val)
            skill_list[re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]", "", temp)] = val

    if evolveMarker:

        res = {
            "attr": attr,
            "name": name,
            "img": url,
            "evolveMarker": evolveMarker,
            "hp": hp,
            "pok_type": pok_type,
            "ability": ability,
            "skill_list": skill_list
        }
        return res
    else:
        res = {
            "attr": attr,
            "name": name,
            "img": url,
            "skill_list": skill_list
        }
        return res


res = []
for i in range(1, 7727, 1):
    try:
        urladd = 'https://asia.pokemon-card.com/tw/card-search/detail/' + str(i) + '/'
        get_data = getInfo(urladd)
        res.append(get_data)
    except:
        print(i)
    finally:
        time.sleep(1 + random.uniform(0, 1))
with open('PTCGdata.json', 'w') as f:
    json.dump(res, f, ensure_ascii=False, indent=4)
f.close()
