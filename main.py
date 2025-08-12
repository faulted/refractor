#!/usr/bin/env python3
import browser_cookie3, os, sys, requests, cloudscraper, shutil, urllib.parse, zipfile, traceback
from bs4 import BeautifulSoup
from pathlib import Path
from ruamel.yaml import YAML
# Make ASCII colorization work on Windows
from colorama import init
init()


class Colors:
    "Class for coloring output"
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GREY = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'


def init_run():
    working_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(working_directory)


def main():
    prism_mods_directory = "/home/chris/primary/Prism/mods/"
    
    cookiejar = browser_cookie3.firefox()
    scraper = cloudscraper.create_scraper(
        browser={
            'custom': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0'
        }
    )
    init_run()
    
    mod_list = "modlist.txt"
    mod_list_text = open(mod_list, "r")

    mod_links = []
    print(Colors.YELLOW + "Mod list found: " + Colors.ENDC)
    for line in mod_list_text.readlines():
        mod_link = {}
        if "https" in line or "curseforge" in line:
            line = line.strip()
            filename = line.rsplit(" ", 1)[0].rsplit(":", 1)[0]
            url = line.rsplit(" ", 1)[1]
            mod_link["filename"] = filename
            mod_link["url"] = url.replace("www", "legacy") + "/file"
            mod_links.append(mod_link)
            print("\t" + Colors.GREY + mod_link["filename"] + Colors.ENDC)
            print("\t\t" + Colors.GREY + mod_link["url"] + Colors.ENDC)

    mod_list_text.close()
    
    print(Colors.YELLOW + "Downloading to Prism mods directory (" + prism_mods_directory + ")"  + Colors.ENDC)

    for link in mod_links:
        response = scraper.get(link["url"], cookies=cookiejar)
        with open(prism_mods_directory + link["filename"], "wb") as file:
            file.write(response.content)
            print(Colors.YELLOW + "       Downloaded: " + link["filename"] + Colors.ENDC)

    clean_up = input("Press any key to clean up mods directory... (" + prism_mods_directory + ")")

    for link in mod_links:
        os.remove(prism_mods_directory + link["filename"])


if __name__ == "__main__":
    main()
