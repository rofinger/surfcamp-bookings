#!/usr/bin/env python3
"""
Hilfsskript zum Generieren von gehashten Passwörtern und Cookie-Keys
für die Streamlit Surf Camp App
"""

import bcrypt
import secrets
import sys

def main():
    print("=" * 60)
    print("🏄 Surf Camp App - Passwort & Key Generator")
    print("=" * 60)
    print()
    
    # Passwort hashen
    print("1️⃣  LOGIN-PASSWORT HASHEN")
    print("-" * 60)
    password = input("Gib dein gewünschtes Login-Passwort ein: ")
    
    if len(password) < 8:
        print("⚠️  Warnung: Passwort sollte mindestens 8 Zeichen lang sein!")
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    print()
    print("✅ Gehashtes Passwort (füge dies in secrets.toml ein):")
    print(f"   {hashed.decode('utf-8')}")
    print()
    
    # Cookie-Key generieren
    print("2️⃣  COOKIE-KEY GENERIEREN")
    print("-" * 60)
    cookie_key = secrets.token_urlsafe(32)
    print("✅ Cookie-Key (füge dies in secrets.toml ein):")
    print(f"   {cookie_key}")
    print()
    
    # Zusammenfassung
    print("=" * 60)
    print("📋 ZUSAMMENFASSUNG - Kopiere diese Werte in secrets.toml:")
    print("=" * 60)
    print()
    print("[auth]")
    print(f'username = "admin"')
    print(f'name = "Dein Name"')
    print(f'hashed_password = "{hashed.decode("utf-8")}"')
    print(f'cookie_key = "{cookie_key}"')
    print()
    print("=" * 60)
    print("⚠️  WICHTIG:")
    print("   - Zum Login verwendest du das ORIGINAL-Passwort:")
    print(f"     '{password}'")
    print("   - NICHT das gehashte Passwort!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Abgebrochen!")
        sys.exit(0)
