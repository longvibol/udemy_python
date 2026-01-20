import time

import requests
import selectorlib
import send_email

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrape(url, headers=HEADERS):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source


class Event:
    def extract(self, source):
        """Extract all the links from the source page"""
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        values = extractor.extract(source)['tours']
        return values


    def store(self, extracted):
        with open("data.txt", "a") as file:
            file.write(extracted + "\n")


def read(extracted):
    with open("data.txt", "r") as file:
        return file.read()


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        event = Event()
        extracted = event.extract(scraped)
        print(extracted)

        content = read(extracted)
        if extracted != "No upcoming tours":
            if extracted not in content:
                event.store(extracted)
                email = send_email.Email()
                email.send(message="The tour has been scraped and Sent Email successfully")
                print("The tour has been scraped successfully")
        time.sleep(1)