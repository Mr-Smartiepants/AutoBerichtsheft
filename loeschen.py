from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from dotenv import load_dotenv
import time
import os
import pdb
import random
import json

# Flask-App initialisieren
app = Flask(__name__)

# .env-Datei laden
load_dotenv()

# Login-Daten aus Umgebungsvariablen abrufen
USERNAME = os.getenv('USERNAME_PERSONAL')
PASSWORD = os.getenv('PASSWORD_PERSONAL')



def delete_all_rows(driver):
    """Löscht alle Zeilen auf der Webseite und bestätigt das Popup."""
    try:
        while True:
            # Finde den ersten "Zeile löschen"-Button
            delete_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@title='Eintrag löschen']"))
            )
            delete_button.click()
            print("Zeile löschen Button geklickt.")

            # Warte auf das Popup und bestätige es
            confirm_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[span[text()='Ja']]"))
            )
            confirm_button.click()
            print("Löschen im Popup bestätigt.")

            # Kurze Pause, um das Nachrutschen der Zeilen abzuwarten
            time.sleep(0.5)

    except Exception as e:
        print("Keine weiteren Zeilen zum Löschen gefunden oder ein Fehler ist aufgetreten:", e)

def process_next_week(driver):
    """Wechselt zur nächsten Woche und startet den gleichen Prozess."""
    try:
        # Button für die nächste Woche finden
        next_week_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@class='timeforward']"))
        )
        print("Button für 'Nächste Woche' gefunden.")
        next_week_button.click()
        print("Klick auf 'Nächste Woche' erfolgreich.")

        # Tätigkeiten auf die Tage verteilen
        delete_all_rows(driver)
    except Exception as e:
        print(f"Fehler beim Zugriff auf 'Nächste Woche': {e}")

try:
    print("Starte Browser...")
    driver = webdriver.Firefox()
    driver.get("https://www.online-ausbildungsnachweis.de/blok/")

    # Login-Prozess
    driver.find_element(By.ID, "id1").send_keys(USERNAME)
    driver.find_element(By.ID, "ida").send_keys(PASSWORD)
    driver.find_element(By.ID, "id2").click()

    # Überprüfen, ob der Login erfolgreich war
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Stefan Weißgerber')]"))
    )
    print("Login erfolgreich!")

    # Kalenderwoche starten
    try:
        first_week = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[starts-with(@title, 'Woche ab')]"))
        )
        print("Element 'Woche ab' gefunden.")
        first_week.click()
        print("Klick auf 'Woche ab' erfolgreich.")
        print(f"Bearbeite Kalenderwoche:")
    except Exception as e:
        print(f"Fehler beim Zugriff auf 'Woche ab': {e}")

    delete_all_rows(driver)

    

except Exception as e:
    print(f"Fehler: {e}")
