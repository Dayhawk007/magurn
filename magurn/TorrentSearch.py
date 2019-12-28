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
    # url_f = []
    search_l = search.split()
    search_name = "+".join(search_l)

    # base_url = "https://1337x.to"
    base_url = "https://x1337.info"  # PROXIED URL
    req_url = base_url + "/sort-search/" + str(search_name) + "/time/desc/1/"
    try:
        res = requests.get(req_url, headers=headers)
    except:
        print(Fore.RED + "ERROR in accessing 1337x: Please Use VPN or Proxy")
        return
    soup = BeautifulSoup(res.content, features="html.parser")
    # print(soup.prettify())
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

        origin.append('1337x')

        seeds.append(seed)

        links.append(base_url + link.get("href"))

        names.append(link.text.strip())

        uploaded.append(row.find('td', attrs={'class': 'coll-date'}).text)

        size = row.find("td", attrs={"class": "size"})
        sizes.append(size.find(text=True))

        data_count += 1
        if data_count == 2:
            break

    if not data_count:
        print(Fore.RED + "Nothing Found on 1337x")


def idope(search):
    # url_f = []
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

        origin.append('idope')

        uploaded.append(
            str(div.find('div', attrs={'class': 'resultdivbottontime'}).text) + " Ago")

        links.append(base_url + link.get("href"))

        names.append(link.text.strip())

        seeds.append(int(seed.text))

        size = div.find("div", {"class": "resultdivbottonlength"})
        sizes.append(size.text.strip().replace(u"\xa0", u" "))

        data_count += 1
        if data_count == 2:
            break

    if not data_count:
        print(Fore.RED + "Nothing Found on idope")


def piratebay(search):
    # url_f = []
    # base_url = "https://thepiratebay.org"
    base_url = "https://247prox.in"  # PROXIED URL
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

        # print(tr)

        link = tr.div.a

        if not check(search, link):
            continue

        td = tr.find_all("td")

        if int(td[-2].text) < min_seeds:  # Seeds should be greater than/equal to min_seeds
            continue

        origin.append('piratebay')

        names.append(link.text.strip())

        links.append(str(base_url + link.get("href")))

        size_data = tr.font.text.split(",")[1].strip()
        size_value = size_data.split()[1]
        size_type = size_data.split()[2].replace("i", "")
        size = str(size_value + " " + size_type)
        sizes.append(size)

        seeds.append(int(td[-2].text))

        uploaded.append(tr.font.text.split(",")[0].strip().split(' ')[1])

        data_count += 1
        if data_count == 2:
            break

    if not data_count:
        print(Fore.RED + "Nothing Found on Piratebay")


def getMagnet(origin, link):
    try:
        url_res = requests.get(link, headers=headers)
    except:
        print(Fore.RED + 'ERROR in fetching magnet link')
        return
    urlsoup = BeautifulSoup(url_res.content, features="html.parser")
    # print(urlsoup.prettify())
    if origin == '1337x':
        div = urlsoup.find('div', attrs={'class': 'row'})
        for a in div.find_all('a'):
            a = a.get('href')
            if 'magnet' in a:
                magnet = a
                return magnet

    elif origin == 'idope':
        # print(urlsoup.prettify())
        magnet = urlsoup.find('a', {'id': "mangetinfo"}).get('href')
        return magnet

    elif origin == 'piratebay':
        div = urlsoup.find("div", attrs={"class": "download"})
        return (div.a.get("href"))


while 1:
    tor_seed = {}
    origin = []
    links = []
    names = []
    seeds = []
    # magnets = []
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
        print(Fore.RED + Style.BRIGHT +
              "\nERROR: Nothing Found. Please check the spelling\n")
        continue

    # Convert Sizes in MB
    size_in_mb = []
    for sizedata in sizes:
        sizesplit = sizedata.split()
        size_without_comma = sizesplit[0].replace(',', '')
        size = float(size_without_comma)
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
    tor_seed["Origin"] = origin
    tor_seed["Links"] = links
    tor_seed["Sizes"] = sizes
    tor_seed["Seeders"] = seeds
    tor_seed["Uploaded"] = uploaded
    tor_seed["SizesMB"] = size_in_mb
    # tor_seed["Magnets"] = magnets
    tor_seed["Score"] = score

    # print(tor_seed)

    maxIndex = score.index(max(score))

    magnet = getMagnet(tor_seed['Origin'][maxIndex],
                       tor_seed['Links'][maxIndex])
    print(Fore.MAGENTA + "Name: " + Style.BRIGHT + tor_seed["Names"][maxIndex])
    print(Fore.MAGENTA + "Size: " + Style.BRIGHT + tor_seed["Sizes"][maxIndex])
    print(Fore.MAGENTA + "Seeds: " + Style.BRIGHT +
          str(tor_seed["Seeders"][maxIndex]))
    print(Fore.MAGENTA + "Uploaded: " + Style.BRIGHT +
          tor_seed["Uploaded"][maxIndex])
    print(Fore.BLUE + 'Torrent Link: ' +
          Style.BRIGHT + tor_seed['Links'][maxIndex])
    try:
        print(Fore.BLUE + "Magnet Link:\n" + Style.BRIGHT + magnet)
    except:
        pass
    try:
        copyToClipBoard(magnet)
        print(Fore.GREEN + "Magnet Copied to ClipBoard")
    except:
        pass
    print("\nPress Ctrl+C to Close\n")
