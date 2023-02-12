import requests
import selectorlib
import smtplib
import ssl
import os
import time
import sqlite3

URL = "https://programmer100.pythonanywhere.com/tours/"

# Establist a connection
connection = sqlite3.connect("data_db.db")


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


def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()

def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
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
            row = read(extracted)
            if not row:
                store(extracted)
                email = Email()
                email.send_email(message="Hey, new event was found!")

        time.sleep(2)

