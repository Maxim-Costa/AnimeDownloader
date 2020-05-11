from bs4 import BeautifulSoup
from time import sleep
import urllib.parse
import urllib.error
import urllib.request
import requests
import json
import os


def GetKeyVideo(url):
    html = requests.request("GET", url, headers={},
                            data={}).text.encode('utf8')
    soup = BeautifulSoup(html)
    animeName = url.split("/")[-2]
    try:
        embed = soup.find_all('iframe')[0]['src']
    except IndexError:
        return "NotVideo", animeName, url

    if "fhvap.com" in embed:
        methode = "VIP#2"
    elif "embed.mystream.to" in embed:
        methode = "MYSTREAM"
    else:
        methode = "unknow : "+""

    if methode == "VIP#2":
        embed = embed.split("/")[-1]
    elif methode == "MYSTREAM":
        embed = None
    return embed, animeName, methode


def requested(url):
    html = requests.request("GET", url, headers={},
                            data={}).text.encode('utf8')
    soup = BeautifulSoup(html, "html.parser")
    return soup


soup = requested("https://docs.google.com/spreadsheets/d/e/2PACX-1vRN8nOfzU1kXYFjoFeRS509_wWtVg-u9lrVANaqiiSFDAcOuopCyqrZq7E15aEr9Bmx_bnUUZCWunka/pubhtml?gid=0&single=true&range=A1:D1500&chrome=false&headers=false")
step = soup.find_all("td", class_="s2")
print(len(step))
link = []
turn = 0
for i in step:
    turn += 1

    if not turn % 10:
        print(turn, end=" ")

    a = i.find_all("a")

    try:
        link.append((requested(a[0]['href']).body["onload"].lstrip(
            "location.replace('").rstrip("'+document.location.hash)"), a[0].string))
    except:
        print('\nerror or no link\n')


Uncategorized = []
link1 = []

for link0, name in link:
    soup = requested(link0)
    step = soup.find_all("a")
    test = False
    for i in step:
        if i.string == "Uncategorized":
            Uncategorized.append((link0, name, link0))
            test = True
    if not test:
        link1.append((link0, name))

print("\n", len(Uncategorized), " || ", len(link1))

for link0, name in link1:
    soup = requested(link0)
    step = soup.find_all("a", class_="ct-btn")
    for i in step:
        if "vostfr" in i['href']:
            Uncategorized.append((i['href'], name, link0))

dico = {}

file = open("result.txt", "w", encoding="utf-8")

for link0, name, originalsLink in Uncategorized:
    soup = requested(link0).find_all("a", class_="multilink-btn current-link")
    name = name.encode('ascii', 'ignore').decode('ascii')
    if len(soup) != 0:
        if "VIP#2" in soup[0].string:
            file.write("*************************************" + "\n")
            file.write("Name : " + name + "\n")
            file.write("link : " + link0 + "\n")
            file.write("methode : VIP#2" + "\n")
            dico[name] = originalsLink
        else:
            file.write("*************************************" + "\n")
            file.write("name : " + name + "\n")
            file.write("methode : " + soup[0].string + "\n")
    else:
        file.write("*************************************" + "\n")
        file.write("Name : " + name + "\n")
        file.write("link : ERROR" + "\n")
file.close()
with open('result.json', 'w') as fp:
    json.dump(dico, fp)
