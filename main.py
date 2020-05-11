from bs4 import BeautifulSoup
from time import sleep
import urllib.parse
import urllib.error
import urllib.request
import requests
import json
import os
import aria2p

aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret="r57OOciJ1aXfONoiIiMmLLQrH1KHdp08EwfIQDjPCdc="
    )
)

def GetKeyVideo(url):
    html = requests.request("GET", url, headers={},
                            data={}).text.encode('utf8')
    soup = BeautifulSoup(html, "html.parser")
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


"""
print("Anime link")
url = input(">>")
"""

url = "https://voiranime.com/rascal-does-not-dream-of-bunny-girl-senpai-2/"

AnimePath = url.split("/")[-2]

html0 = requests.request("GET", url, headers={}, data={}).text.encode('utf8')
soup0 = BeautifulSoup(html0, "html.parser")
step0 = soup0.find_all("a", class_="ct-btn")
link0 = []
for i in step0:
    if "vostfr" in i['href']:
        link0.append(i['href'])
        html1 = requests.request(
            "GET", i['href'], headers={}, data={}).text.encode('utf8')
        soup1 = BeautifulSoup(html1, "html.parser")
        step1 = soup1.find_all(
            "a", class_="btn btn-sm btn-default")
        for j in step1:
            link0.append(j['href'])


link = []
for i in link0:
    link.append(GetKeyVideo(i))

os.system('cls')
for embed, animeName, methode in link:
    if embed != "NotVideo":

        print("*************")
        print("Name : ", animeName)
        print("link or id : ", embed)
        print("methode : ", methode)
        file_name = animeName+".mp4"
        if os.path.isdir(f"/media/gordi/98453328-5ec2-4612-be91-863b432fac96/Anime/{AnimePath}/{animeName}"):
            print('already download')
        else:
            if methode == "VIP#2":
                url = "https://www.fhvap.com/api/source/"+embed
                payload = {}
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                response = requests.request(
                    "POST", url, headers=headers, data=payload)
                VideoRAW = response.text.encode('utf8')
                if VideoRAW != None:
                    if json.loads(VideoRAW)['success']:
                        VideoJSON = json.loads(VideoRAW)['data']
                        print("qualiter : ", VideoJSON[-1]['label'])
                        url = [VideoJSON[-1]['file']]
                        downloads = aria2.add_uris(url, dict(dir=f"/media/gordi/98453328-5ec2-4612-be91-863b432fac96/Anime/{AnimePath}/{animeName}"))
                    else:
                        print('Download Error, link failed')
                else:
                    print('request failed')

                url, file_name, payload, headers, response, VideoRAW, VideoJSON = None, None, None, None, None, None, None
                sleep(1)
            else:
                print("Methode not compatible with")
    else:
        print("*************")
        print("Name : ", animeName)
        print("Link or id : ", methode)
        print('Not a Video')
