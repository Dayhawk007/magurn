import pyperclip
import pandas as pd
from bs4 import BeautifulSoup
import requests
from config import *
import search

print("Initializing....")


def copyToClipBoard(text):
    pyperclip.copy(text)


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"
}


while 1:
    searchterm = input("Enter the name of torrent you want to search\n")

    print("Scraping from idope....")
    search.idope(searchterm)

    print("Scraping from 1337x....")
    search._1337x(searchterm)

    print("Scraping from PirateBay....")
    search.piratebay(searchterm)

    if not len(names):
        print("\nNothing Found\n")
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

    tor_seed["Names"] = names
    tor_seed["Sizes"] = sizes
    tor_seed["SizesMB"] = size_in_mb
    tor_seed["Seeders"] = seeds
    tor_seed["Magnets"] = magnets

    df = pd.DataFrame(tor_seed)

    # Calculate Scores to determine better torrent by calculating Seeders/Size
    df["Score"] = df.apply(lambda row: row.Seeders / row.SizesMB, axis=1)
    df = df.sort_values("Score", ascending=False).reset_index(drop=True)
    # print(df)

    print("Name: " + df["Names"][0])
    print("Size: " + df["Sizes"][0])
    print("Seeds:", df["Seeders"][0])
    print("Magnet Link:\n" + df["Magnets"][0])
    copyToClipBoard(df["Magnets"][0])
    print("Magnet Copied to ClipBoard")
    print("Press Ctrl+C to Close\n")
