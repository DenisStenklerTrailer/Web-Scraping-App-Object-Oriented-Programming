import requests
import selectorlib
import smtplib
import ssl
import os
import time
import sqlite3

URL = "https://programmer100.pythonanywhere.com/tours/"


class Event:
    def scrape(self, url):
        """Scrape the page source from the URL"""
        response = requests.get(url)
        source = response.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"] # tours is the name of the class in the extract.yaml file
        return value


class Email:
    def send(self, message):
        host = "smtp.gmail.com"
        port = 465

        username = "olga.trojer@gmail.com"
        password = "mvcyzomecnqupgri"

        reciever = "denis.stenkler@gmail.com"
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, reciever, message)


class Database:

    def __init__(self, database_path):
        # Establist a connection
        self.connection = sqlite3.connect(database_path)
        
    def store(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
        self.connection.commit()

    def read(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        band, city, date = row
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from events WHERE band=? AND City=? AND Date=?", (band, city, date))
        rows = cursor.fetchall()
        return rows


if __name__ == "__main__":
    while True:
        event = Event()
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            database = Database(database_path="data_db.db")
            row = database.read(extracted)
            if not row:
                database.store(extracted)
                email = Email()
                email.send_email(message="Hey, new event was found!")

        time.sleep(2)

