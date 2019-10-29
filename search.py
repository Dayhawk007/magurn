import requests
from bs4 import BeautifulSoup

import proxy

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"
}

piratebay_proxy_url = proxy.get_piratebay_proxy_url()
# print(piratebay_proxy_url)


def check(search, link):
    srch_vrf = 0
    for nt in search.lower().split():
        if nt in link.text.lower():
            srch_vrf += 1
    if srch_vrf < len(search.lower().split()):
        return False
    else:
        return True


def _1337x(search):
    url_f = []
    search_l = search.split()
    search_name = "+".join(search_l)

    # base_url = "https://1337x.to"
    base_url = "https://1337xto.eu"  # PROXIED URL
    req_url = base_url + "/search/" + str(search_name) + "/1/"
    try:
        res = requests.get(req_url, headers=headers)
    except:
        print("\nERROR in accessing 1337x: Please Use VPN or Proxy\n")
        return
    soup = BeautifulSoup(res.content, features="html.parser")
    c = False
    data_cnt = 0
    for row in soup.find_all("tr"):
        if not c:
            c = True
            continue

        link_data = row.find_all("a")
        link = link_data[1]

        if not check(search, link):
            continue

        url_f.append(base_url + link.get("href"))
        names.append(link.text.strip())

        size = row.find("td", attrs={"class": "size"})
        sizes.append(size.find(text=True))

        data_cnt += 1
        if data_cnt == 2:
            break

    for url in url_f:
        url_res = requests.get(url, headers=headers)
        urlsoup = BeautifulSoup(url_res.content, features="html.parser")
        for seed in urlsoup.find_all("span", {"class": "seeds"}):
            seeds.append(int(seed.text))

        for magnet in urlsoup.find_all("a"):
            try:
                if "magnet" in magnet.text.split()[0].lower():
                    magnets.append(magnet.get("href"))
            except:
                pass


def idope(search):
    url_f = []
    # base_url = "https://idope.se"
    base_url = "https://gv6zipaqcoaau4qe.onio.icu"  # PROXIED URL
    req_url = base_url + "/torrent-list/" + str(search) + "/"
    try:
        res = requests.get(req_url, headers=headers)
    except:
        print("\nERROR in accessing idope: Please Use VPN or Proxy\n")
        return

    soup = BeautifulSoup(res.content, features="html.parser")

    data_cnt = 0
    for div in soup.find_all("div", attrs={"class": "resultdiv"}):
        link = div.find("a")

        if not check(search, link):
            continue

        url_f.append(base_url + link.get("href"))
        names.append(link.text.strip())

        seed = div.find("div", {"class": "resultdivbottonseed"})
        seeds.append(int(seed.text))

        size = div.find("div", {"class": "resultdivbottonlength"})
        sizes.append(size.text.strip().replace(u"\xa0", u" "))

        data_cnt += 1
        if data_cnt == 2:
            break

    for url in url_f:
        url_res = requests.get(url, headers=headers)
        urlsoup = BeautifulSoup(url_res.content, features="html.parser")
        for magnet in urlsoup.find_all(id="mangetinfo"):
            magnets.append(magnet.text.strip())


def piratebay(search):
    url_f = []
    # base_url = "https://thepiratebay.org"
    base_url = "https://247prox.link"  # PROXIED URL
    # base_url = piratebay_proxy_url

    req_url = base_url + "/search/" + search
    try:
        res = requests.get(req_url, headers=headers)
    except:
        print("\nERROR in accessing PirateBay: Please Use VPN or Proxy\n")
        return

    soup = BeautifulSoup(res.content, features="html.parser")
    data_count = 0
    c = False
    for tr in soup.find_all("tr"):
        if not c:
            c = True
            continue

        link = tr.div.a

        if not check(search, link):
            continue

        names.append(link.text.strip())

        url_f.append(str(base_url + link.get("href")))

        size_data = tr.font.text.split(",")[1].strip()
        size_value = size_data.split()[1]
        size_type = size_data.split()[2].replace("i", "")
        size = str(size_value + " " + size_type)
        sizes.append(size)

        td = tr.find_all("td")
        seeds.append(int(td[-2].text))

        data_count += 1
        if data_count == 2:
            break

    for url in url_f:
        url_res = requests.get(url, headers=headers)
        urlsoup = BeautifulSoup(url_res.content, features="html.parser")

        uploaded.append(urlsoup.find_all('dd')[-6].text.split()[0])

        div = urlsoup.find("div", attrs={"class": "download"})

        magnets.append(div.a.get("href"))
