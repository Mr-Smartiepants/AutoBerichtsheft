

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


# Globale Variablen

# JSON-Daten laden
with open("activities.json", "r") as file:
    activities = json.load(file)

weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday"]

def calculate_remaining_time(total_minutes, max_minutes=480):
    """Berechnet die verbleibende Zeit für den Tag."""
    return max_minutes - total_minutes

def format_duration(minutes):
    """Formatiert die Dauer in das Format 'xh:xxmin'."""
    return f"{minutes // 60}h:{minutes % 60:02d}min"

def add_activity(driver, day, index):
    """Fügt die Tätigkeit 'Schule' und die Zeit 8h in die Webseite ein."""
    try:
        # Klicke auf den Button, um eine neue Zeile hinzuzufügen
        add_button = driver.find_element(By.XPATH, f"//a[contains(@name, 'tableComp:{day.lower()}:addRow')]")
        add_button.click()
        print(f"Button für neue Zeile geklickt (Schule).")
        
        # Warte auf das neue Textfeld für die Tätigkeit
        new_activity_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//textarea[contains(@name, '{day.lower()}:inputs:{index}:report')]"))
        )
        new_activity_field.click()
        new_activity_field.send_keys("Schule")
        print(f"Tätigkeit 'Schule' erfolgreich eingetragen.")

        # Warte auf das zugehörige Zeitfeld für die Dauer
        new_time_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//input[contains(@name, '{day.lower()}:inputs:{index}:has')]"))
        )
        new_time_field.click()
        new_time_field.send_keys("8h:00min")
        print(f"Zeit für '8h:00min' erfolgreich eingetragen.")
    except Exception as e:
        print(f"Fehler beim Hinzufügen der Tätigkeit 'Schule': {e}")

def distribute_activities(driver):
    """Trägt für jeden Tag die Tätigkeit 'Schule' mit 8 Stunden ein."""
    for day in weekdays:
        print(f"Bearbeite {day}...")
        index = 0  # Startindex für die Zeilen

        # Füge die Tätigkeit 'Schule' ein
        add_activity(driver, day, index)
        print(f"Tätigkeit 'Schule' für {day} erfolgreich eingetragen.")
    

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

        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@title='Eintrag hinzufügen']"))
        )
        print("Seite für die nächste Woche vollständig geladen.")

        # Lösche alle Zeilen in der neuen Woche
        delete_all_rows(driver)

        # Tätigkeiten auf die Tage verteilen
        distribute_activities(driver)
        
        process_next_week(driver)
    except Exception as e:
        print(f"Fehler beim Zugriff auf 'Nächste Woche': {e}")

# Hauptlogik
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
    # Tätigkeiten auf die Tage verteilen
    distribute_activities(driver)

except Exception as e:
    print(f"Fehler: {e}")

# finally:
#     # Browser schließen
#     driver.quit()

# ACHTUNG: Flask-Route und App-Start
@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.json
    activities = data.get('activities', [])
    report = f"Bericht für die Woche:\n" + "\n".join(activities)
    return jsonify({"report": report})

if __name__ == '__main__':
    print("Starte Flask-App...")
    app.run(debug=True, use_reloader=False)