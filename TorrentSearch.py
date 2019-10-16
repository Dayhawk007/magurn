print("Initializing....")
import requests
from bs4 import BeautifulSoup
import pandas as pd
searchterm=input("Enter the name of torrent you want to search\n")
tor_seed={}
names=[]
urls=[]
seeds=[]
magnets=[]
def _1337x(search):
    url_f=[]
    search_l=search.split()

    search_name="+".join(search_l)
    req_url="https://www.1337x.to/search/"+str(search_name)+"/1/"
    res=requests.get(req_url,headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
    })
    soup=BeautifulSoup(res.content,features='html.parser')
    link_con=0
    for link in soup.find_all('a'):
        if search.lower() in link.text.lower():
            names.append(link.text.strip())
            url_f.append("https://www.1337x.to"+link.get('href'))
            link_con += 1
        if link_con==2:
            break
    for url in url_f:
        url_res=requests.get(url,headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
        })
        urlsoup=BeautifulSoup(url_res.content,features='html.parser')
        for seed in urlsoup.find_all('span',{'class':'seeds'}):
            seeds.append(int(seed.text))

        for magnet in urlsoup.find_all('a'):
            try:
                if 'magnet' in magnet.text.split()[0].lower():
                    magnets.append(magnet.get('href'))
            except:
                    pass
    for x in url_f:
        urls.append(x)

def idope(search):
    url_f=[]
    req_url="https://idope.se/torrent-list/"+str(search)+"/"
    res=requests.get(req_url,headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
    })
    soup=BeautifulSoup(res.content,features='html.parser')
    link_con=0
    for link in soup.find_all('a'):
        if search.lower() in link.text.lower().strip():
            names.append(link.text.strip())
            url_f.append("https://idope.se"+link.get('href'))
            link_con += 1
        if link_con==2:
            break
    scnt=0
    for seed in soup.find_all('div',{'class':'resultdivbottonseed'}):
        seeds.append(int(seed.text))
        scnt+=1
        if scnt==2:
            break
    for url in url_f:
        url_res=requests.get(url,headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
        })
        urlsoup=BeautifulSoup(url_res.content,features='html.parser')
        for magnet in urlsoup.find_all('a',{'id':'mangetinfo'}):
            magnets.append(magnet.text.strip())
    for x in url_f:
        urls.append(x)

print("Scraping from idope....")
idope(searchterm)
print("Scraping from 1337x....")
_1337x(searchterm)
tor_seed["Names"]=names
tor_seed["Links"]=urls
tor_seed["Seeders"]=seeds
tor_seed["Magnets"]=magnets
df=pd.DataFrame(tor_seed)
df.sort_values('Seeders')
print("Name:\n"+df["Names"][0])
print("Magnet Link:\n"+df["Magnets"][0])
input("Press Any Key to Close")
