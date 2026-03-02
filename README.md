# AutoBerichtsheft

Automatisierung zur Befüllung eines Online-Ausbildungsnachweises (Berichtsheft) mit Python & Selenium.  
Das Tool steuert den Browser, meldet sich an, navigiert zum Eintragsformular und füllt Tage anhand vordefinierter Tätigkeiten aus.  
Die Tätigkeiten liegen in einer JSON-Datei und werden so kombiniert, dass pro Tag möglichst 8 Stunden erreicht werden.

---

## Warum dieses Projekt?

Das Schreiben des Berichtshefts ist repetitiv und kostet Zeit.  
Ziel war eine praxisnahe Automatisierung eines wiederkehrenden Web-Workflows:

- Login & Navigation im Browser
- Formular automatisiert ausfüllen
- Tätigkeiten aus JSON auswählen und kombinieren
- Tagesdauer automatisch auf ~8h auffüllen

---

## Features

- Browser-Automatisierung mit Selenium (Klickpfade, Formulare, Navigation)
- Konfiguration über `.env` (Zugangsdaten, optional WebDriver-Pfad)
- Tätigkeiten in `activities.json` konfigurierbar
- Zeitlogik: Aufgabenblöcke mit Dauer, Kombination bis ~8h/Tag
- Skripte zum Löschen/Resetten von Einträgen (z. B. Wochen- oder manuelles Löschen)

---

## Tech Stack

- Python
- Selenium
- JSON (Konfiguration der Tätigkeiten)
- `.env` (Konfiguration/Secrets)

---

## Projektstruktur

```bash
AutoBerichtsheft/
├── app.py
├── activities.json
├── requirements.txt
├── .env.example
├── README.md
├── schule.py
├── loeschen.py
├── loeschen_manuell.py
└── loeschen_wochen.py
