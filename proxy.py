import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"
}


def get_piratebay_proxy_url():
    data = requests.get("https://piratebay-proxylist.se/", headers=headers)

    soup = BeautifulSoup(data.content, features="html.parser")

    links = []
    flag = False
    for tr in soup.find_all('tr'):
        if not flag:
            flag = True
            continue

        links.append('https://' + tr.span.text.strip())

    for link in links:
        try:
            res = requests.get(link, headers=headers)
        except Exception as e:
            continue

        return str(link)
