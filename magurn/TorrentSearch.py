import pyperclip
from bs4 import BeautifulSoup
import requests
# import magurn.proxy as proxy

from colorama import init, Fore, Back, Style
init(autoreset=True)

print(Fore.GREEN + "Initializing....")


def copyToClipBoard(text):
    pyperclip.copy(text)


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"
}

min_seeds = 5

# Takes about 5 seconds to get proxy url
# piratebay_proxy_base_url = proxy.get_piratebay_proxy_url()


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
    req_url = base_url + "/sort-search/" + str(search_name) + "/time/desc/1/"
    try:
        res = requests.get(req_url, headers=headers)
    except:
        print(Fore.RED + "ERROR in accessing 1337x: Please Use VPN or Proxy")
        return
    soup = BeautifulSoup(res.content, features="html.parser")
    c = False
    data_count = 0
    for row in soup.find_all("tr"):
        if not c:
            c = True
            continue

        link_data = row.find_all("a")
        link = link_data[1]

        if not check(search, link):
            continue

        seed = int(row.find('td', attrs={'class': 'coll-2'}).text)

        if seed < min_seeds:  # Seeds should be greater than/equal to min_seeds
            continue

        seeds.append(seed)

        url_f.append(base_url + link.get("href"))
        names.append(link.text.strip())

        uploaded.append(row.find('td', attrs={'class': 'coll-date'}).text)

        size = row.find("td", attrs={"class": "size"})
        sizes.append(size.find(text=True))

        data_count += 1
        if data_count == 2:
            break

    for url in url_f:
        url_res = requests.get(url, headers=headers)
        urlsoup = BeautifulSoup(url_res.content, features="html.parser")

        for magnet in urlsoup.find_all("a"):
            try:
                if "magnet" in magnet.text.split()[0].lower():
                    magnets.append(magnet.get("href"))
            except:
                pass

    if not data_count:
        print(Fore.RED + "Nothing Found on 1337x")


def idope(search):
    url_f = []
    # base_url = "https://idope.se"
    base_url = "https://gv6zipaqcoaau4qe.onio.icu"  # PROXIED URL
    req_url = base_url + "/torrent-list/" + str(search) + "/?&o=-3"
    try:
        res = requests.get(req_url, headers=headers)
    except:
        print(Fore.RED + "ERROR in accessing idope: Please Use VPN or Proxy")
        return

    soup = BeautifulSoup(res.content, features="html.parser")

    data_count = 0
    for div in soup.find_all("div", attrs={"class": "resultdiv"}):
        link = div.find("a")

        if not check(search, link):
            continue

        seed = div.find("div", {"class": "resultdivbottonseed"})

        if int(seed.text) < min_seeds:  # Seeds should be greater than/equal to min_seeds
            continue

        uploaded.append(
            str(div.find('div', attrs={'class': 'resultdivbottontime'}).text) + " Ago")
        url_f.append(base_url + link.get("href"))
        names.append(link.text.strip())

        seeds.append(int(seed.text))

        size = div.find("div", {"class": "resultdivbottonlength"})
        sizes.append(size.text.strip().replace(u"\xa0", u" "))

        data_count += 1
        if data_count == 2:
            break

    for url in url_f:
        url_res = requests.get(url, headers=headers)
        urlsoup = BeautifulSoup(url_res.content, features="html.parser")
        for magnet in urlsoup.find_all(id="mangetinfo"):
            magnets.append(magnet.text.strip())

    if not data_count:
        print(Fore.RED + "Nothing Found on idope")


def piratebay(search):
    url_f = []
    # base_url = "https://thepiratebay.org"
    base_url = "https://247prox.link"  # PROXIED URL
    # base_url = piratebay_proxy_base_url

    req_url = base_url + "/search/" + search + "/0/3/0"
    try:
        res = requests.get(req_url, headers=headers)
    except:
        print(Fore.RED + "ERROR in accessing PirateBay: Please Use VPN or Proxy")
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

        td = tr.find_all("td")

        if int(td[-2].text) < min_seeds:  # Seeds should be greater than/equal to min_seeds
            continue

        names.append(link.text.strip())

        url_f.append(str(base_url + link.get("href")))

        size_data = tr.font.text.split(",")[1].strip()
        size_value = size_data.split()[1]
        size_type = size_data.split()[2].replace("i", "")
        size = str(size_value + " " + size_type)
        sizes.append(size)

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

    if not data_count:
        print(Fore.RED + "Nothing Found on Piratebay")


while 1:
    tor_seed = {}
    names = []
    seeds = []
    magnets = []
    sizes = []
    uploaded = []

    searchterm = input("Enter the name of torrent you want to search\n")

    print("Scraping from idope....")
    idope(searchterm)

    print("Scraping from 1337x....")
    _1337x(searchterm)

    print("Scraping from PirateBay....")
    piratebay(searchterm)

    if not len(names):
        print(Fore.RED + Style.BRIGHT + "\nERROR: Nothing Found. Please check the spelling\n")
        continue

    # Convert Sizes in MB
    size_in_mb = []
    for sizedata in sizes:
        sizesplit = sizedata.split()
        size = float(sizesplit[0])
        type_size = sizesplit[1]
        if type_size == "B":
            size_mb = size / (1024 * 1024)
        if type_size == "KB":
            size_mb = size / 1024
        if type_size == "MB":
            size_mb = size
        if type_size == "GB":
            size_mb = size * 1024
        if type_size == "TB":
            size_mb = size * 1024 * 1024
        size_in_mb.append(size_mb)

    score = []
    for i in range(len(sizes)):
        score.append(seeds[i]/size_in_mb[i])

    tor_seed["Names"] = names
    tor_seed["Sizes"] = sizes
    tor_seed["Seeders"] = seeds
    tor_seed["Uploaded"] = uploaded
    tor_seed["SizesMB"] = size_in_mb
    tor_seed["Magnets"] = magnets
    tor_seed["Score"] = score

    maxIndex = score.index(max(score))

    print(Fore.MAGENTA + "Name: " + Style.BRIGHT + tor_seed["Names"][maxIndex])
    print(Fore.MAGENTA + "Size: " + Style.BRIGHT + tor_seed["Sizes"][maxIndex])
    print(Fore.MAGENTA + "Seeds: " + Style.BRIGHT + str(tor_seed["Seeders"][maxIndex]))
    print(Fore.MAGENTA + "Uploaded: " + Style.BRIGHT + tor_seed["Uploaded"][maxIndex])
    print(Fore.BLUE + "Magnet Link:\n" + Style.BRIGHT + tor_seed["Magnets"][maxIndex])
    try:
        copyToClipBoard(tor_seed["Magnets"][maxIndex])
        print(Fore.GREEN + "Magnet Copied to ClipBoard")
    except:
        pass
    print("\nPress Ctrl+C to Close\n")
