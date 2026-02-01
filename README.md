# 🏄 Surf Camp Buchungsmanagement App

Eine professionelle Streamlit-Webanwendung zur Verwaltung von Surf Camp Buchungen mit Google Sheets Integration, E-Mail-Automatisierung und sicherem Login.

## ✨ Features

- 🔐 **Sicherer Login** mit `streamlit-authenticator`
- 📊 **Dashboard** mit Buchungsübersicht und Statistiken
- 📝 **Buchungsverwaltung** direkt aus Google Sheets
- 📧 **E-Mail-Automatisierung** mit editierbaren Templates
- 🎨 **Benutzerfreundliche UI** mit Streamlit
- ☁️ **Cloud-Datenhaltung** via Google Sheets

## 🚀 Quick Start

### 1. Installation

```bash
# Repository klonen oder Dateien herunterladen
cd surf-camp-app

# Virtuelle Umgebung erstellen (empfohlen)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -r requirements.txt
```

### 2. Konfiguration

Erstelle die Ordnerstruktur:
```
surf-camp-app/
├── app.py
├── requirements.txt
├── generate_credentials.py
└── .streamlit/
    └── secrets.toml  # <- Diese Datei musst du erstellen!
```

**Wichtige Schritte:**

1. **Google Sheets API einrichten** (siehe `KONFIGURATION.md`)
2. **Gmail App-Passwort erstellen** (siehe `KONFIGURATION.md`)
3. **Login-Passwort hashen:**
   ```bash
   python generate_credentials.py
   ```
4. **secrets.toml erstellen** (nutze `secrets.toml.example` als Vorlage)

📖 **Detaillierte Anleitung:** Siehe `KONFIGURATION.md`

### 3. Google Sheet vorbereiten

Erstelle ein Google Sheet mit folgenden Spalten:

| Name | Email | Telefon | Zeitraum | Anzahl_Personen | Kurstyp | Preis | Status | Notizen | Letzte_Aktualisierung |
|------|-------|---------|----------|-----------------|---------|-------|--------|---------|----------------------|

Beispiel-Daten:
```
Max Mustermann | max@email.com | 0123456789 | 01.06-07.06.2026 | 2 | Anfänger | 299 | Neu | | 
```

**Wichtig:** Teile das Sheet mit der Service Account E-Mail (aus der JSON-Datei)!

### 4. App starten

```bash
streamlit run app.py
```

Die App öffnet sich automatisch im Browser: `http://localhost:8501`

## 🎯 Verwendung

### Login
- **Username:** `admin` (oder wie in secrets.toml konfiguriert)
- **Passwort:** Dein Klartext-Passwort (NICHT das gehashte!)

### Dashboard
- Zeigt alle Buchungen aus Google Sheets
- Statistiken: Gesamt, Neu, Bestätigt, Angebot gesendet
- Filter nach Status

### Buchung bearbeiten
1. Wähle eine Buchung in der Sidebar
2. Ändere den Status (Neu → Angebot gesendet → Bestätigt)
3. Füge Notizen hinzu
4. Klicke "Status speichern"

### E-Mail senden
1. Wähle E-Mail-Typ: Angebot / Bestätigung / Absage
2. Bearbeite den E-Mail-Text im Textfeld
3. Klicke "E-Mail senden"
4. Status wird automatisch aktualisiert

## 📧 E-Mail Templates

Die App bietet vorgefertigte Templates:

- **Angebot:** Personalisiertes Angebot mit Preisen und Details
- **Bestätigung:** Buchungsbestätigung mit allen Informationen
- **Absage:** Höfliche Absage mit Alternativvorschlägen

Alle Templates sind vor dem Versand editierbar!

## 🔒 Sicherheit

- ✅ Passwörter werden mit bcrypt gehasht
- ✅ Authentifizierung mit Session-Management
- ✅ secrets.toml wird NICHT ins Git-Repository committed
- ✅ Gmail nutzt App-Passwörter (nicht das Haupt-Passwort)

**⚠️ WICHTIG:** Füge `.streamlit/secrets.toml` zu `.gitignore` hinzu!

## 📁 Dateistruktur

```
surf-camp-app/
├── app.py                      # Hauptanwendung
├── requirements.txt            # Python-Dependencies
├── generate_credentials.py     # Passwort-Hash-Generator
├── KONFIGURATION.md           # Detaillierte Setup-Anleitung
├── secrets.toml.example       # Vorlage für secrets.toml
├── README.md                  # Diese Datei
└── .streamlit/
    └── secrets.toml           # Geheime Konfiguration (NICHT committen!)
```

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python 3.9+
- **Datenbank:** Google Sheets (via `streamlit-gsheets-connection`)
- **Authentifizierung:** streamlit-authenticator
- **E-Mail:** smtplib (Gmail SMTP)

## 📊 Google Sheets Spalten

| Spalte | Typ | Beschreibung |
|--------|-----|--------------|
| Name | Text | Kundenname |
| Email | Text | E-Mail-Adresse |
| Telefon | Text | Telefonnummer |
| Zeitraum | Text | Buchungszeitraum (z.B. "01.06-07.06.2026") |
| Anzahl_Personen | Zahl | Anzahl Teilnehmer |
| Kurstyp | Text | Art des Kurses (z.B. "Anfänger", "Fortgeschritten") |
| Preis | Text/Zahl | Preis in EUR |
| Status | Text | Buchungsstatus (Neu, Angebot gesendet, Bestätigt, etc.) |
| Notizen | Text | Interne Notizen |
| Letzte_Aktualisierung | Text | Zeitstempel der letzten Änderung |

## 🐛 Troubleshooting

### Problem: "Authentication failed" beim E-Mail-Versand
**Lösung:** Stelle sicher, dass du ein Gmail **App-Passwort** verwendest, nicht dein normales Passwort.

### Problem: "Permission denied" bei Google Sheets
**Lösung:** Teile das Google Sheet mit der Service Account E-Mail aus der JSON-Datei.

### Problem: Login funktioniert nicht
**Lösung:** Verwende zum Login das **Original-Passwort**, nicht das gehashte!

### Problem: "Failed to load data"
**Lösung:** Überprüfe die Spreadsheet-URL in `secrets.toml`.

Weitere Lösungen: Siehe `KONFIGURATION.md`

## 📚 Dokumentation

- [KONFIGURATION.md](KONFIGURATION.md) - Detaillierte Setup-Anleitung
- [secrets.toml.example](secrets.toml.example) - Konfigurationsvorlage
- [Streamlit Docs](https://docs.streamlit.io/)
- [Google Sheets API](https://developers.google.com/sheets/api)

## 🚀 Deployment

### Lokales Deployment
Die App läuft lokal auf deinem Computer:
```bash
streamlit run app.py
```

### Cloud Deployment (Streamlit Cloud)
1. Pushe den Code zu GitHub (OHNE secrets.toml!)
2. Gehe zu [share.streamlit.io](https://share.streamlit.io)
3. Verbinde dein GitHub-Repository
4. Füge die Secrets in den Streamlit Cloud Settings hinzu
5. Deploy!

## ⚙️ Konfigurierbare Features

In `app.py` kannst du anpassen:
- E-Mail-Templates
- Status-Optionen
- Spalten-Namen im Google Sheet
- Dashboard-Metriken
- E-Mail-Betreffzeilen

## 📈 Erweiterungsmöglichkeiten

- 📅 Kalender-Integration
- 💳 Zahlungsabwicklung
- 📱 SMS-Benachrichtigungen
- 📊 Erweiterte Statistiken und Reports
- 🔔 Automatische Erinnerungen
- 🌐 Mehrsprachigkeit

## 🤝 Support

Bei Fragen oder Problemen:
1. Checke `KONFIGURATION.md`
2. Schaue im Troubleshooting-Bereich nach
3. Kontaktiere den Support

## 📄 Lizenz

Diese App wurde für den internen Gebrauch im Surf Camp entwickelt.

---

**Viel Erfolg mit deinem Surf Camp! 🏄‍♂️🌊**
