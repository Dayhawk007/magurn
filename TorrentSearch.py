print("Initializing....")
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pyperclip

def copyToClipBoard(text):
    pyperclip.copy(text)

def _1337x(search):
    url_f=[]
    search_l=search.split()
    search_name="+".join(search_l)

    req_url="https://1337x.unblocked.ltda/search/"+str(search_name)+"/1/"
    # req_url="https://1337x.to/search/"+str(search_name)+"/1/"
    try:
        res=requests.get(req_url,headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
        })
    except:
        print("\nERROR in accessing 1337x: Please Use VPN or Proxy\n")
        return
    soup=BeautifulSoup(res.content,features='html.parser')
    # print(soup.prettify())
    c=False
    data_cnt=0
    for row in soup.find_all('tr'):
        if not c: 
            c=True
            continue

        link_data = row.find_all('a')
        link = link_data[1]
        srch_vrf=0
        for nt in search.lower().split():
            if nt in link.text.lower():
                srch_vrf+=1
        if srch_vrf < len(search.lower().split()):
            continue
        url_f.append("https://1337x.unblocked.ltda"+link.get('href'))
        # url_f.append("https://1337x.to"+link.get('href'))
        names.append(link.text.strip())

        size = row.find('td', attrs = {'class':'size'})
        sizes.append(size.find(text=True))

        data_cnt+=1
        if(data_cnt == 2): break

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
            except: pass
    for x in url_f:
        urls.append(x)

def idope(search):
    url_f=[]

    req_url="https://idope.se/torrent-list/"+str(search)+"/"
    try:
        res=requests.get(req_url,headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
        })
    except:
        print("\nERROR in accessing idope: Please Use VPN or Proxy\n")
        return

    soup = BeautifulSoup(res.content,features='html.parser')

    data_cnt=0
    for div in soup.find_all('div', attrs={'class': 'resultdiv'}):
        srch_vrf=0
        link = div.find('a')
        for nt in search.lower().split():
            if nt in link.text.lower():
                srch_vrf+=1
        if srch_vrf < len(search.lower().split()):
            continue

        url_f.append("https://idope.se"+link.get('href'))
        names.append(link.text.strip())

        seed = div.find('div',{'class':'resultdivbottonseed'})
        seeds.append(int(seed.text))

        size = div.find('div',{'class':'resultdivbottonlength'})
        sizes.append(size.text.strip().replace(u'\xa0', u' '))

        data_cnt+=1
        if(data_cnt == 2): break

    for url in url_f:
        url_res=requests.get(url,headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
        })
        urlsoup=BeautifulSoup(url_res.content,features='html.parser')
        for magnet in urlsoup.find_all('a',{'id':'mangetinfo'}):
            magnets.append(magnet.text.strip())
            
    for x in url_f:
        urls.append(x)

while(1):
    tor_seed={}
    names=[]
    urls=[]
    seeds=[]
    magnets=[]
    sizes=[]

    searchterm=input("Enter the name of torrent you want to search\n")

    print("Scraping from idope....")
    idope(searchterm)

    print("Scraping from 1337x....")
    _1337x(searchterm)

    if(not len(names)): 
        print("Nothing Found")
        continue 

    tor_seed["Names"]=names
    tor_seed["Sizes"]=sizes
    tor_seed["Links"]=urls
    tor_seed["Seeders"]=seeds
    tor_seed["Magnets"]=magnets

    df=pd.DataFrame(tor_seed)
    df.sort_values('Seeders')

    print("Name: "+df["Names"][0])
    print("Size: "+df["Sizes"][0])
    print("Seeds:", df["Seeders"][0])
    print("Magnet Link:\n"+df["Magnets"][0])
    copyToClipBoard(df["Magnets"][0])
    print("Magnet Copied to ClipBoard")
    print("Press Ctrl+C to Close\n")
