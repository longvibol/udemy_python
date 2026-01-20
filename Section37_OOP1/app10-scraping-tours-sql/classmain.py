import time
import requests
import selectorlib
from datetime import datetime
import sqlite3

URL = "https://programmer100.pythonanywhere.com/"
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
        extractor = selectorlib.Extractor.from_yaml_file("extracthome.yaml")
        values = extractor.extract(source)['home']
        return values


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("temdatabase.db")

    def store(self, extracted):
        row = extracted.split(',')
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO temperature VALUES (?,?)", row)
        self.connection.commit()

    def read(self, extracted):
        row = extracted.split(',')
        row = [item.strip() for item in row]
        date, tem = row
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM temperature WHERE date=? AND tem=?", (date, tem))
        rows = cursor.fetchall()
        return rows

if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        event = Event()
        extracted = event.extract(scraped)
        s = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        extracted = f"{s},{extracted}"
        print(extracted)

        if extracted != "No upcoming tours":
            database = Database()
            row = database.read(extracted)
            if not row:
                database.store(extracted)
        time.sleep(2)