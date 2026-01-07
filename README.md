# Berichtsheft

Kurz: Automatisierung zur Befüllung des Online-Ausbildungsnachweises.

Setup

- Python 3.8+ empfohlen
- Virtuelle Umgebung erstellen und aktivieren:

```bash
python -m venv .venv
source .venv/bin/activate
```

- Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

- `.env` anlegen (nicht ins Repo committen):

```bash
cp .env.example .env
# dann .env bearbeiten und USERNAME/PASSWORD setzen
```

Run

```bash
python app.py
```

Hinweise

- Die Datei `.env` ist in `.gitignore` eingetragen.
- Trage keine Passwörter in das Repository ein; benutze `.env`.
- Optional: Falls der Firefox-Webdriver (geckodriver) nicht im PATH ist, setze `GECKODRIVER_PATH` in `.env`.
