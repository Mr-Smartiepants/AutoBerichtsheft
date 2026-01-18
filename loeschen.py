from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


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
    switch_to_week_content(driver)
    while True:
        delete_buttons = driver.find_elements(By.XPATH, "//a[@title='Eintrag löschen']")
        if not delete_buttons:
            print("Keine weiteren Zeilen zum Löschen gefunden.")
            break

        delete_button = delete_buttons[0]
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(delete_button))
        delete_button.click()
        print("Zeile löschen Button geklickt.")

        # Warte auf das Popup und bestätige es
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Ja']]"))
        )
        confirm_button.click()
        print("Löschen im Popup bestätigt.")

        # Warten bis Overlay weg ist und UI fertig gerendert hat
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.k-overlay"))
        )
        time.sleep(0.2)


def find_first_open_week(driver):
    """Findet die erste offene Woche mit Fallback-XPaths."""
    candidate_xpaths = [
        # Häufig: Titel enthält Hinweis auf offenen Status
        "//a[starts-with(@title, 'Woche ab') and contains(@title, 'offen')]",
        "//a[starts-with(@title, 'Woche ab') and contains(@title, 'Offen')]",
        # Fallback: erste Woche, die nicht abgeschlossen ist
        "//a[starts-with(@title, 'Woche ab') and not(contains(@title, 'abgeschlossen'))]",
        # Letzter Fallback: erste Woche überhaupt
        "//a[starts-with(@title, 'Woche ab')]",
    ]

    last_error = None
    for xpath in candidate_xpaths:
        try:
            return WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
        except Exception as e:
            last_error = e
            continue

    raise last_error


def switch_to_week_content(driver):
    """Stellt sicher, dass wir im richtigen Frame für die Wochendetails sind."""
    def has_week_controls():
        return driver.find_elements(
            By.XPATH, "//a[@title='Eintrag löschen' or @title='Eintrag hinzufügen']"
        )

    driver.switch_to.default_content()
    try:
        WebDriverWait(driver, 5).until(lambda d: has_week_controls())
        return
    except Exception:
        pass

    frames = driver.find_elements(By.TAG_NAME, "iframe")
    for frame in frames:
        driver.switch_to.default_content()
        driver.switch_to.frame(frame)
        if has_week_controls():
            print("Wochendetails im iframe gefunden.")
            return

    driver.switch_to.default_content()
    print("Hinweis: Wochendetails nicht gefunden (kein iframe mit Controls).")

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

driver = None
try:
    print("Starte Browser...")
    firefox_options = Options()
    firefox_options.binary_location = "/snap/firefox/current/usr/lib/firefox/firefox"
    driver = webdriver.Firefox(options=firefox_options)
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
        first_week = find_first_open_week(driver)
        print("Element für erste offene Woche gefunden.")
        driver.execute_script("arguments[0].scrollIntoView(true);", first_week)
        first_week.click()
        print("Klick auf erste offene Woche erfolgreich.")
        print("Bearbeite erste offene Kalenderwoche.")
        switch_to_week_content(driver)
    except Exception as e:
        print(f"Fehler beim Zugriff auf die erste offene Woche: {e}")

    delete_all_rows(driver)

except Exception as e:
    print(f"Fehler: {e}")
finally:
    if driver:
        driver.quit()
