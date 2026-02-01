import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit_authenticator as stauth
from datetime import datetime
import yaml
from yaml.loader import SafeLoader

# Seitenkonfiguration
st.set_page_config(
    page_title="Surf Camp Buchungsmanagement",
    page_icon="🏄",
    layout="wide"
)

# Authentifizierung konfigurieren
def load_authenticator():
    """Lädt die Authentifizierungskonfiguration"""
    config = {
        'credentials': {
            'usernames': {
                st.secrets["auth"]["username"]: {
                    'name': st.secrets["auth"]["name"],
                    'password': st.secrets["auth"]["hashed_password"]
                }
            }
        },
        'cookie': {
            'expiry_days': 30,
            'key': st.secrets["auth"]["cookie_key"],
            'name': 'surf_camp_auth'
        },
        'preauthorized': {
            'emails': []
        }
    }
    
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    
    return authenticator

# Google Sheets Verbindung
@st.cache_resource
def get_gsheet_connection():
    """Stellt Verbindung zu Google Sheets her"""
    return st.connection("gsheets", type=GSheetsConnection)

# Daten laden
def load_bookings(conn):
    """Lädt Buchungen aus Google Sheets"""
    df = conn.read(worksheet="Buchungen", usecols=list(range(10)), ttl=5)
    df = df.dropna(how="all")
    return df

# Daten aktualisieren
def update_booking(conn, row_index, status, notes=""):
    """Aktualisiert den Status einer Buchung"""
    df = load_bookings(conn)
    df.loc[row_index, 'Status'] = status
    df.loc[row_index, 'Notizen'] = notes
    df.loc[row_index, 'Letzte_Aktualisierung'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    conn.update(worksheet="Buchungen", data=df)
    return True

# E-Mail senden
def send_email(recipient_email, subject, body, sender_name="Surf Camp Team"):
    """Sendet eine E-Mail über Gmail SMTP"""
    try:
        # SMTP Konfiguration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = st.secrets["email"]["address"]
        sender_password = st.secrets["email"]["password"]
        
        # E-Mail erstellen
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{sender_name} <{sender_email}>"
        message["To"] = recipient_email
        
        # HTML und Plain Text Version
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                {body.replace(chr(10), '<br>')}
                <br><br>
                <hr style="border: 1px solid #eee;">
                <p style="font-size: 12px; color: #777;">
                    Mit freundlichen Grüßen,<br>
                    Dein {sender_name}
                </p>
            </body>
        </html>
        """
        
        plain_text = MIMEText(body, "plain")
        html_text = MIMEText(html_body, "html")
        message.attach(plain_text)
        message.attach(html_text)
        
        # E-Mail senden
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        return True, "E-Mail erfolgreich versendet!"
    
    except Exception as e:
        return False, f"Fehler beim E-Mail-Versand: {str(e)}"

# E-Mail Templates
def get_email_template(template_type, customer_name, booking_details):
    """Generiert E-Mail-Templates"""
    templates = {
        "angebot": f"""Hallo {customer_name},

vielen Dank für deine Anfrage zu unserem Surf Camp!

Wir freuen uns, dir folgendes Angebot zu unterbreiten:

📅 Zeitraum: {booking_details.get('Zeitraum', 'TBD')}
👥 Teilnehmer: {booking_details.get('Anzahl_Personen', 'TBD')}
🏄 Kurs: {booking_details.get('Kurstyp', 'TBD')}

💰 Preis: {booking_details.get('Preis', 'TBD')} EUR

Das Angebot beinhaltet:
- Professionelle Surfkurse mit zertifizierten Trainern
- Surfboard und Neoprenanzug
- Versicherung

Hast du Fragen oder möchtest du buchen? Melde dich gerne!

Wir freuen uns auf dich! 🌊""",
        
        "bestaetigung": f"""Hallo {customer_name},

deine Buchung ist bestätigt! 🎉

📋 Buchungsdetails:
📅 Zeitraum: {booking_details.get('Zeitraum', 'TBD')}
👥 Teilnehmer: {booking_details.get('Anzahl_Personen', 'TBD')}
🏄 Kurs: {booking_details.get('Kurstyp', 'TBD')}
💰 Gesamtpreis: {booking_details.get('Preis', 'TBD')} EUR

📍 Treffpunkt: {booking_details.get('Treffpunkt', 'Wird noch bekannt gegeben')}

Bitte bringe mit:
✓ Badesachen und Handtuch
✓ Sonnenschutz
✓ Gute Laune!

Wir freuen uns riesig auf dich! Bei Fragen sind wir jederzeit für dich da.

Bis bald am Strand! 🏄‍♂️🌊""",
        
        "absage": f"""Hallo {customer_name},

vielen Dank für dein Interesse an unserem Surf Camp.

Leider müssen wir dir mitteilen, dass wir für deinen gewünschten Zeitraum ({booking_details.get('Zeitraum', 'TBD')}) keine Kapazitäten mehr frei haben.

Möchtest du einen alternativen Termin in Betracht ziehen? Wir haben noch folgende Termine verfügbar:
- [Alternative Termine hier einfügen]

Melde dich gerne, wenn du Interesse an einem anderen Zeitraum hast!"""
    }
    
    return templates.get(template_type, "")

# Hauptanwendung
def main():
    # Authentifizierung
    authenticator = load_authenticator()
    
    name, authentication_status, username = authenticator.login(
        location='main',
        fields={'Form name': 'Surf Camp Login', 'Username': 'Benutzername', 'Password': 'Passwort', 'Login': 'Anmelden'}
    )
    
    if authentication_status == False:
        st.error('Benutzername oder Passwort ist falsch')
        return
    
    if authentication_status == None:
        st.warning('Bitte gib deine Zugangsdaten ein')
        return
    
    # App-Header
    col1, col2 = st.columns([6, 1])
    with col1:
        st.title("🏄 Surf Camp Buchungsmanagement")
        st.markdown(f"Willkommen zurück, **{name}**!")
    with col2:
        authenticator.logout(button_name='Abmelden', location='main')
    
    st.divider()
    
    # Google Sheets Verbindung
    conn = get_gsheet_connection()
    
    # Daten laden
    try:
        df = load_bookings(conn)
        
        # Statistiken
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Gesamt Anfragen", len(df))
        with col2:
            neu_count = len(df[df['Status'] == 'Neu']) if 'Status' in df.columns else 0
            st.metric("🆕 Neue Anfragen", neu_count)
        with col3:
            bestaetigt_count = len(df[df['Status'] == 'Bestätigt']) if 'Status' in df.columns else 0
            st.metric("✅ Bestätigt", bestaetigt_count)
        with col4:
            offen_count = len(df[df['Status'] == 'Angebot gesendet']) if 'Status' in df.columns else 0
            st.metric("⏳ Angebot gesendet", offen_count)
        
        st.divider()
        
        # Hauptbereich: Tabelle
        st.subheader("📋 Alle Buchungsanfragen")
        
        # Filter
        col1, col2 = st.columns(2)
        with col1:
            if 'Status' in df.columns:
                status_filter = st.multiselect(
                    "Filter nach Status:",
                    options=df['Status'].unique().tolist(),
                    default=df['Status'].unique().tolist()
                )
                df_filtered = df[df['Status'].isin(status_filter)]
            else:
                df_filtered = df
        
        # Tabelle anzeigen
        st.dataframe(
            df_filtered,
            use_container_width=True,
            hide_index=True,
            height=400
        )
        
        st.divider()
        
        # Sidebar: Bearbeitung
        with st.sidebar:
            st.header("✏️ Buchung bearbeiten")
            
            # Buchung auswählen
            if len(df) > 0 and 'Name' in df.columns:
                buchung_auswahl = st.selectbox(
                    "Wähle eine Buchung:",
                    options=range(len(df)),
                    format_func=lambda x: f"{df.iloc[x]['Name']} - {df.iloc[x].get('Status', 'Unbekannt')}"
                )
                
                selected_row = df.iloc[buchung_auswahl]
                
                st.info(f"**Kunde:** {selected_row.get('Name', 'N/A')}\n\n"
                       f"**E-Mail:** {selected_row.get('Email', 'N/A')}\n\n"
                       f"**Zeitraum:** {selected_row.get('Zeitraum', 'N/A')}")
                
                # Status ändern
                st.subheader("Status aktualisieren")
                new_status = st.selectbox(
                    "Neuer Status:",
                    options=["Neu", "Angebot gesendet", "Bestätigt", "Abgesagt", "Abgeschlossen"],
                    index=["Neu", "Angebot gesendet", "Bestätigt", "Abgesagt", "Abgeschlossen"].index(
                        selected_row.get('Status', 'Neu')
                    ) if selected_row.get('Status', 'Neu') in ["Neu", "Angebot gesendet", "Bestätigt", "Abgesagt", "Abgeschlossen"] else 0
                )
                
                notes = st.text_area(
                    "Notizen:",
                    value=selected_row.get('Notizen', ''),
                    height=100
                )
                
                if st.button("💾 Status speichern", use_container_width=True):
                    if update_booking(conn, buchung_auswahl, new_status, notes):
                        st.success("✅ Status aktualisiert!")
                        st.rerun()
                
                st.divider()
                
                # E-Mail senden
                st.subheader("📧 E-Mail senden")
                
                email_type = st.selectbox(
                    "E-Mail-Typ:",
                    options=["angebot", "bestaetigung", "absage"],
                    format_func=lambda x: {
                        "angebot": "📝 Angebot senden",
                        "bestaetigung": "✅ Bestätigung senden",
                        "absage": "❌ Absage senden"
                    }[x]
                )
                
                # E-Mail Details
                booking_details = {
                    'Zeitraum': selected_row.get('Zeitraum', 'TBD'),
                    'Anzahl_Personen': selected_row.get('Anzahl_Personen', 'TBD'),
                    'Kurstyp': selected_row.get('Kurstyp', 'Surfkurs'),
                    'Preis': selected_row.get('Preis', 'TBD'),
                    'Treffpunkt': 'Surf Camp Basis, Strandpromenade 1'
                }
                
                email_subject = st.text_input(
                    "Betreff:",
                    value={
                        "angebot": f"Dein Surf Camp Angebot - {booking_details['Zeitraum']}",
                        "bestaetigung": f"Buchungsbestätigung - {booking_details['Zeitraum']}",
                        "absage": "Deine Surf Camp Anfrage"
                    }[email_type]
                )
                
                template = get_email_template(
                    email_type,
                    selected_row.get('Name', 'Surfer'),
                    booking_details
                )
                
                email_body = st.text_area(
                    "E-Mail-Text (editierbar):",
                    value=template,
                    height=300
                )
                
                if st.button(f"📨 {email_type.title()}-E-Mail senden", type="primary", use_container_width=True):
                    with st.spinner("E-Mail wird gesendet..."):
                        success, message = send_email(
                            selected_row.get('Email', ''),
                            email_subject,
                            email_body
                        )
                        
                        if success:
                            st.success(message)
                            # Status automatisch aktualisieren
                            auto_status = {
                                "angebot": "Angebot gesendet",
                                "bestaetigung": "Bestätigt",
                                "absage": "Abgesagt"
                            }[email_type]
                            update_booking(conn, buchung_auswahl, auto_status, f"E-Mail gesendet: {email_type}")
                            st.rerun()
                        else:
                            st.error(message)
            else:
                st.warning("Keine Buchungen vorhanden")
    
    except Exception as e:
        st.error(f"Fehler beim Laden der Daten: {str(e)}")
        st.info("Bitte stelle sicher, dass dein Google Sheet korrekt konfiguriert ist.")

if __name__ == "__main__":
    main()
