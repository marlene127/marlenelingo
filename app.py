import streamlit as st
import pandas as pd
import random

# Passwortschutz
passwort = "marlene2025"
eingabe = st.text_input("🔒 Bitte Passwort eingeben:", type="password")
if eingabe != passwort:
    st.warning("Zutritt nur für Berechtigte.")
    st.stop()

# Daten laden
vokabeln = pd.read_csv("vokabeln.csv")
grammatik = pd.read_csv("grammatik.csv")
lesen = pd.read_csv("lesen.csv")

# Session State initialisieren
if "punkte" not in st.session_state:
    st.session_state.punkte = 0
if "gesamt" not in st.session_state:
    st.session_state.gesamt = 0
if "neue_aufgabe" not in st.session_state:
    st.session_state.neue_aufgabe = True

# Session State Initialisierung
for key, default in {
    "punkte": 0,
    "gesamt": 0,
    "neue_aufgabe": True,
    "akt_daten": None,
    "richtung": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = default
        
st.title("🇮🇹 MarleneLingo 6.2 PRO 🚀")
st.write(f"🌟 Punkte: {st.session_state.punkte} / {st.session_state.gesamt}")

modus = st.selectbox("Wähle deinen Lernmodus:", ["Vokabeln", "Grammatik", "Leseverständnis"])

# Vokabelmodus
if modus == "Vokabeln":
    if st.session_state.neue_aufgabe:
        level = st.selectbox("Wähle dein Sprachlevel:", vokabeln["level"].unique(), key="level")
        daten = vokabeln[vokabeln["level"] == level].sample(1).iloc[0]
        richtung = random.choice(["de_it", "it_de"])
        st.session_state.akt_daten = daten
        st.session_state.richtung = richtung
        st.session_state.neue_aufgabe = False
    else:
        daten = st.session_state.akt_daten
        richtung = st.session_state.richtung

    if richtung == "de_it":
        eingabe = st.text_input(f"Wie heißt '{daten['de']}' auf Italienisch?", key="eingabe")
        korrekt = daten["it"]
    else:
        eingabe = st.text_input(f"Was bedeutet '{daten['it']}' auf Deutsch?", key="eingabe")
        korrekt = daten["de"]

    if st.button("Antwort prüfen"):
        st.session_state.gesamt += 1
        if eingabe.lower() == korrekt.lower():
            st.success("✅ Richtig!")
            st.session_state.punkte += 1
        else:
            st.error(f"❌ Falsch! Richtig wäre: {korrekt}")
        if st.button("Nächste Aufgabe"):
            st.session_state.neue_aufgabe = True
            st.experimental_rerun()

# Grammatikmodus
elif modus == "Grammatik":
    if st.session_state.neue_aufgabe:
        daten = grammatik.sample(1).iloc[0]
        st.session_state.akt_daten = daten
        st.session_state.neue_aufgabe = False
    else:
        daten = st.session_state.akt_daten

    st.write(daten["frage"])
    antwort = st.radio("Wähle die richtige Form:", [daten["option1"], daten["option2"], daten["option3"]], key="antwort")

    if st.button("Antwort prüfen"):
        st.session_state.gesamt += 1
        if antwort == daten["antwort"]:
            st.success("✅ Richtig!")
            st.session_state.punkte += 1
        else:
            st.error(f"❌ Falsch! Richtig wäre: {daten['antwort']}")
        if st.button("Nächste Aufgabe"):
            st.session_state.neue_aufgabe = True
            st.experimental_rerun()

# Leseverständnis
elif modus == "Leseverständnis":
    if st.session_state.neue_aufgabe:
        daten = lesen.sample(1).iloc[0]
        st.session_state.akt_daten = daten
        st.session_state.neue_aufgabe = False
    else:
        daten = st.session_state.akt_daten

    st.write("📖 **Text:**")
    st.write(daten["text"])
    st.write(daten["frage"])
    antwort = st.radio("Wähle:", [daten["option1"], daten["option2"], daten["option3"]], key="antwort_lesen")

    if st.button("Antwort prüfen"):
        st.session_state.gesamt += 1
        if antwort == daten["antwort"]:
            st.success("✅ Richtig!")
            st.session_state.punkte += 1
        else:
            st.error(f"❌ Falsch! Richtig wäre: {daten['antwort']}")
        if st.button("Nächste Aufgabe"):
            st.session_state.neue_aufgabe = True
            st.experimental_rerun()

# Fortschrittsbalken
if st.session_state.gesamt > 0:
    st.progress(st.session_state.punkte / st.session_state.gesamt)

