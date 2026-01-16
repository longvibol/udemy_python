import time
import requests
import selectorlib
from datetime import datetime

URL = "https://programmer100.pythonanywhere.com/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrape(url, headers=HEADERS):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source

def extract(source):
    """Extract all the links from the source page"""
    extractor = selectorlib.Extractor.from_yaml_file("extracthome.yaml")
    values = extractor.extract(source)['home']
    return values


def store(extracted):
    now = datetime.now().strftime("%y-%m-%d-%H-%M-%S")
    with open("home.txt", "a") as file:

        file.write(f'{now},{extracted}'+"\n")


def read(extracted):
    with open("home.txt", "r") as file:
        return file.read()


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)

        content = read(extracted)
        for i in content:
            if extracted != "No upcoming tours":
                store(extracted)
                s = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                print(f"{s},{extracted}")
            time.sleep(1)

        with open("home.txt", "a") as file:
            file.write("date,temperature" + "\n")