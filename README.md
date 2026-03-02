# AutoBerichtsheft

Automatisierung zur Befüllung eines Online-Ausbildungsnachweises (Berichtsheft) mit Python & Selenium.  
Das Tool steuert den Browser, meldet sich an, navigiert zum Eintragsformular und füllt Tage anhand vordefinierter Tätigkeiten aus.  
Die Tätigkeiten liegen in einer JSON-Datei und werden so kombiniert, dass pro Tag möglichst **8 Stunden** erreicht werden.

---

## Motivation

Das Schreiben des Berichtshefts ist ein wiederkehrender, manueller Prozess mit klarer Struktur.  
Ziel dieses Projekts war es, diesen Web-Workflow technisch zu analysieren und durch Browser-Automatisierung effizient umzusetzen.

---

## Features

- Browser-Automatisierung mit Selenium
- Automatischer Login über Umgebungsvariablen
- Navigation durch mehrstufige Web-Oberflächen
- Formularbefüllung mit strukturierten Tätigkeiten
- JSON-basierte Konfiguration der Aufgaben
- Zeitlogik zur Kombination von Aufgabenblöcken bis ~8h/Tag
- Hilfsskripte zum Löschen oder Zurücksetzen von Einträgen

---

## Tech Stack

- Python
- Selenium
- JSON (Konfigurationsbasis)
- `.env` für Credentials und Konfiguration

---

## Projektstruktur

```bash
AutoBerichtsheft/
├── app.py
├── activities.json
├── requirements.txt
├── .env.example
├── schule.py
├── loeschen.py
├── loeschen_manuell.py
├── loeschen_wochen.py
└── README.md
```

### Kurzbeschreibung der Dateien

- **app.py**  
  Hauptprogramm: Login → Navigation → Formularbefüllung → Speichern

- **activities.json**  
  Enthält Tätigkeiten inkl. Dauerangaben als Bausteine für die Tagesplanung

- **schule.py**  
  Enthält unterstützende Logik zur Strukturierung oder Planung

- **loeschen\*.py**  
  Skripte zum Löschen oder Zurücksetzen von Einträgen

- **.env.example**  
  Vorlage für notwendige Umgebungsvariablen

---

## Konfiguration

### 1) Virtuelle Umgebung erstellen

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) `.env` Datei anlegen

```bash
cp .env.example .env
```

In der `.env` werden Zugangsdaten und ggf. WebDriver-Pfade hinterlegt.

Wichtig:  
`.env` wird **nicht** ins Repository committed.

---

## activities.json – Konzept

Die Tätigkeiten sind als Aufgabenblöcke mit Dauer definiert.  
Das Programm kombiniert diese Bausteine, bis pro Tag möglichst 8 Stunden erreicht werden.

Beispielstruktur:

```json
[
  { "text": "Feature-Implementierung", "minutes": 240 },
  { "text": "Bugfixing & Tests", "minutes": 120 },
  { "text": "Code Review", "minutes": 120 }
]
```

Die Auswahl erfolgt regelbasiert, um die Tagesdauer konsistent zu erreichen.

---

## Ablauf (High-Level)

1. Start des Selenium-WebDrivers
2. Login über Credentials aus `.env`
3. Navigation zum Berichtsheft-Formular
4. Auswahl und Kombination von Tätigkeiten aus `activities.json`
5. Befüllen der Formularfelder
6. Speichern/Bestätigen des Eintrags

---

## Starten

```bash
python app.py
```

---

## Herausforderungen & Lernschwerpunkte

- Stabilität bei UI-Automation (Selektoren, Wartezeiten, Timing)
- Strukturierte Trennung zwischen Konfiguration (JSON) und Logik (Python)
- Umsetzung eines realen Web-Workflows
- Regelbasierte Zeitplanung bis 8h/Tag
- Umgang mit Änderungen in Web-Oberflächen

---

## Hinweise

- Selektoren können sich bei Änderungen der Zielseite anpassen müssen
- Credentials niemals im Code speichern
- Das Tool ist für den legitimen, privaten Gebrauch gedacht
