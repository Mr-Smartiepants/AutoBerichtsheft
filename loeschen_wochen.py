from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.firefox.options import Options

from dotenv import load_dotenv
import time
import os

# Flask-App initialisieren
app = Flask(__name__)

# .env-Datei laden
load_dotenv()

# Login-Daten aus Umgebungsvariablen abrufen
USERNAME = os.getenv("USERNAME_PERSONAL")
PASSWORD = os.getenv("PASSWORD_PERSONAL")


def switch_to_week_content(driver, timeout=12):
    """Stellt sicher, dass wir im richtigen Frame für die Wochendetails sind."""
    def has_week_controls():
        return driver.find_elements(
            By.XPATH, "//a[@title='Eintrag löschen' or @title='Eintrag hinzufügen']"
        )

    end_time = time.time() + timeout
    while time.time() < end_time:
        driver.switch_to.default_content()

        # Falls die Wochendetails im iframe liegen, zuerst dort suchen
        frames = driver.find_elements(By.TAG_NAME, "iframe")
        for frame in frames:
            try:
                driver.switch_to.default_content()
                driver.switch_to.frame(frame)
                if has_week_controls():
                    print("Wochendetails im iframe gefunden.")
                    return
            except Exception:
                continue

        # Fallback: Wochendetails sind ggf. direkt im Dokument
        driver.switch_to.default_content()
        if has_week_controls():
            return

        time.sleep(0.2)

    driver.switch_to.default_content()
    print("Hinweis: Wochendetails nicht gefunden (kein iframe mit Controls).")


def delete_one_row(driver):
    """Löscht genau eine Zeile. True=gelöscht, False=keine Zeilen, None=temporärer Fehler."""
    switch_to_week_content(driver)
    delete_buttons = driver.find_elements(By.XPATH, "//a[@title='Eintrag löschen']")
    if not delete_buttons:
        return False

    delete_button = delete_buttons[0]
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", delete_button)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(delete_button))
        delete_button.click()
        print("Zeile löschen Button geklickt.")

        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Ja']]"))
        )
        confirm_button.click()
        print("Löschen im Popup bestätigt.")

        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.k-overlay"))
        )
        try:
            WebDriverWait(driver, 5).until(EC.staleness_of(delete_button))
        except TimeoutException:
            pass
        time.sleep(0.2)
        return True
    except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
        print(f"Temporärer Fehler beim Löschen: {e}")
        return None


def delete_all_rows(driver):
    """Löscht alle Zeilen auf der Webseite und bestätigt das Popup."""
    retries = 0
    while True:
        try:
            WebDriverWait(driver, 5).until(
                lambda d: d.find_elements(By.XPATH, "//a[@title='Eintrag löschen']") or
                          d.find_elements(By.XPATH, "//a[@title='Eintrag hinzufügen']")
            )
        except Exception:
            pass

        result = delete_one_row(driver)
        if result is True:
            retries = 0
            continue
        if result is False:
            print("Keine weiteren Zeilen zum Löschen gefunden.")
            break

        retries += 1
        if retries >= 3:
            print("Mehrfacher Fehler beim Löschen, breche für diese Woche ab.")
            break


def go_to_next_week(driver):
    """Wechselt zur nächsten Woche. Gibt False zurück, wenn keine weitere Woche vorhanden ist."""
    driver.switch_to.default_content()
    try:
        next_week_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='timeforward']"))
        )
    except Exception:
        print("Keine weitere Woche gefunden.")
        return False

    driver.execute_script("arguments[0].scrollIntoView(true);", next_week_button)
    next_week_button.click()
    print("Klick auf 'Nächste Woche' erfolgreich.")

    # Warten, bis Wochendetails verfügbar sind
    try:
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.k-overlay"))
        )
    except Exception:
        pass

    switch_to_week_content(driver, timeout=15)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@title='Eintrag hinzufügen']"))
    )
    return True


def open_first_week_in_list(driver):
    """Klickt die erste sichtbare Woche in der Liste an."""
    driver.switch_to.default_content()
    week_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[starts-with(@title, 'Woche ab')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", week_link)
    week_link.click()
    print("Woche in der Liste angeklickt.")
    switch_to_week_content(driver, timeout=15)


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

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Stefan Weißgerber')]"))
    )
    print("Login erfolgreich!")

    input("Bitte zur Startwoche navigieren und Enter druecken ...")

    delete_all_rows(driver)

    while True:
        if not go_to_next_week(driver):
            break
        open_first_week_in_list(driver)
        delete_all_rows(driver)

except Exception as e:
    print(f"Fehler: {e}")
finally:
    if driver:
        driver.quit()
