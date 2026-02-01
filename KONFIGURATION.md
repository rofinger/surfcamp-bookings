# KONFIGURATIONSANLEITUNG für .streamlit/secrets.toml

## 📁 Dateistruktur erstellen

Erstelle folgende Ordnerstruktur in deinem Projekt:
```
surf-camp-app/
├── app.py
├── requirements.txt
└── .streamlit/
    └── secrets.toml
```

## 🔐 secrets.toml Konfiguration

Erstelle die Datei `.streamlit/secrets.toml` mit folgendem Inhalt:

---

# ============================================
# GOOGLE SHEETS KONFIGURATION
# ============================================

[connections.gsheets]
spreadsheet = "DEINE_SPREADSHEET_URL_ODER_ID"
# Beispiel: "https://docs.google.com/spreadsheets/d/1ABC...XYZ/edit"
# Oder nur die ID: "1ABC...XYZ"

# Service Account Credentials (JSON)
type = "service_account"
project_id = "DEIN_PROJECT_ID"
private_key_id = "DEIN_PRIVATE_KEY_ID"
private_key = "-----BEGIN PRIVATE KEY-----\nDEIN_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
client_email = "DEIN_SERVICE_ACCOUNT@DEIN_PROJECT.iam.gserviceaccount.com"
client_id = "DEIN_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/DEIN_SERVICE_ACCOUNT%40DEIN_PROJECT.iam.gserviceaccount.com"

# ============================================
# E-MAIL KONFIGURATION (Gmail)
# ============================================

[email]
address = "deine-email@gmail.com"
password = "dein-app-passwort"
# WICHTIG: Verwende ein App-Passwort, NICHT dein normales Gmail-Passwort!
# Siehe Anleitung unten, wie du ein App-Passwort erstellst.

# ============================================
# AUTHENTIFIZIERUNG
# ============================================

[auth]
username = "admin"
name = "Admin User"
# Gehashtes Passwort (siehe Anleitung unten)
hashed_password = "$2b$12$DEIN_GEHASHTES_PASSWORT"
# Cookie-Key für Session Management (zufälliger String)
cookie_key = "dein-zufaelliger-cookie-key-123456"

---

## 📝 SCHRITT-FÜR-SCHRITT ANLEITUNG

### 1️⃣ GOOGLE SHEETS API EINRICHTEN

1. Gehe zu: https://console.cloud.google.com/
2. Erstelle ein neues Projekt oder wähle ein bestehendes
3. Aktiviere die "Google Sheets API":
   - Navigiere zu "APIs & Services" > "Library"
   - Suche nach "Google Sheets API"
   - Klicke auf "Enable"

4. Erstelle ein Service Account:
   - Gehe zu "APIs & Services" > "Credentials"
   - Klicke auf "Create Credentials" > "Service Account"
   - Gib einen Namen ein (z.B. "surf-camp-sheets")
   - Klicke auf "Create and Continue"
   - Rolle: "Editor" (oder "Owner")
   - Klicke auf "Done"

5. Erstelle einen JSON-Key:
   - Klicke auf den erstellten Service Account
   - Gehe zu "Keys" Tab
   - Klicke "Add Key" > "Create new key"
   - Wähle "JSON" Format
   - Die Datei wird heruntergeladen

6. Kopiere die Werte aus der JSON-Datei in secrets.toml:
   ```json
   {
     "type": "service_account",
     "project_id": "...",
     "private_key_id": "...",
     "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
     "client_email": "...",
     "client_id": "...",
     ...
   }
   ```

7. Teile dein Google Sheet mit dem Service Account:
   - Öffne dein Google Sheet
   - Klicke auf "Share"
   - Füge die `client_email` aus der JSON-Datei hinzu
   - Gib "Editor" Rechte

### 2️⃣ GOOGLE SHEET STRUKTUR

Erstelle ein Google Sheet mit dem Namen "Buchungen" und folgenden Spalten:

| Name | Email | Telefon | Zeitraum | Anzahl_Personen | Kurstyp | Preis | Status | Notizen | Letzte_Aktualisierung |
|------|-------|---------|----------|-----------------|---------|-------|--------|---------|----------------------|
| Max Mustermann | max@email.com | 0123456789 | 01.06-07.06.2026 | 2 | Anfänger | 299 | Neu | | |

Die App wird diese Spalten automatisch verwenden.

### 3️⃣ GMAIL APP-PASSWORT ERSTELLEN

WICHTIG: Du kannst NICHT dein normales Gmail-Passwort verwenden!

1. Gehe zu deinem Google Account: https://myaccount.google.com/
2. Klicke auf "Security" (Sicherheit)
3. Stelle sicher, dass "2-Step Verification" aktiviert ist
   - Falls nicht: Aktiviere es zuerst!
4. Suche nach "App passwords" (App-Passwörter)
5. Klicke auf "App passwords"
6. Wähle:
   - App: "Mail"
   - Device: "Other (Custom name)" → Gib "Surf Camp App" ein
7. Klicke auf "Generate"
8. Kopiere das 16-stellige Passwort (Format: xxxx xxxx xxxx xxxx)
9. Füge es in secrets.toml ein (ohne Leerzeichen)

### 4️⃣ PASSWORT HASHEN

Du musst dein Login-Passwort hashen. Führe dieses Python-Script aus:

```python
import bcrypt

# Dein gewünschtes Passwort
password = "dein-sicheres-passwort"

# Passwort hashen
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(hashed.decode('utf-8'))
```

Oder verwende diesen Online-Befehl:
```bash
python -c "import bcrypt; print(bcrypt.hashpw(b'dein-passwort', bcrypt.gensalt()).decode('utf-8'))"
```

Kopiere das Ergebnis in `hashed_password` in secrets.toml.

### 5️⃣ COOKIE KEY GENERIEREN

Erstelle einen zufälligen String für den Cookie-Key:

```python
import secrets
print(secrets.token_urlsafe(32))
```

Oder:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 🚀 APP STARTEN

1. Installiere die Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Starte die App:
   ```bash
   streamlit run app.py
   ```

3. Die App öffnet sich im Browser auf: http://localhost:8501

4. Logge dich ein mit:
   - Username: admin (oder was du in secrets.toml gesetzt hast)
   - Passwort: dein-sicheres-passwort (NICHT das gehashte!)

## ⚠️ SICHERHEITSHINWEISE

1. ❌ NIEMALS `secrets.toml` ins Git-Repository committen!
   - Füge zu .gitignore hinzu: `.streamlit/secrets.toml`

2. ✅ Die secrets.toml enthält sensible Daten:
   - Google API Keys
   - E-Mail-Passwörter
   - Authentifizierungsdaten

3. 🔒 Verwende starke Passwörter für:
   - Gmail App-Passwort
   - Login-Passwort

4. 📧 Gmail Limits beachten:
   - Max. 500 E-Mails pro Tag (normale Accounts)
   - Max. 2000 E-Mails pro Tag (Google Workspace)

## 🐛 TROUBLESHOOTING

### Problem: "Authentication failed" beim E-Mail-Versand
→ Lösung: Überprüfe, ob du ein App-Passwort (nicht normales Passwort) verwendest

### Problem: "Permission denied" bei Google Sheets
→ Lösung: Stelle sicher, dass das Sheet mit der Service Account E-Mail geteilt ist

### Problem: "Failed to load data"
→ Lösung: Überprüfe die Spreadsheet-URL in secrets.toml

### Problem: Login funktioniert nicht
→ Lösung: Stelle sicher, dass du das NICHT-gehashte Passwort zum Einloggen verwendest

## 📚 WEITERE RESSOURCEN

- Streamlit Docs: https://docs.streamlit.io/
- Google Sheets API: https://developers.google.com/sheets/api
- Gmail SMTP: https://support.google.com/mail/answer/7126229

---

Bei Fragen oder Problemen, melde dich gerne! 🏄
