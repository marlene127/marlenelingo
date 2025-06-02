import streamlit as st
import pandas as pd
import random

# Passwortschutz
passwort = "marlene2025"

eingabe = st.text_input("🔒 Bitte Passwort eingeben:", type="password")

if eingabe != passwort:
    st.warning("Zutritt nur für Berechtigte.")
    st.stop()

# ---------------------------------------
# Daten laden
# ---------------------------------------

# Vokabeln
vokabeln = pd.read_csv("vokabeln.csv")

# Grammatik
grammatik = pd.read_csv("grammatik.csv")

# Leseverständnis
lesen = pd.read_csv("lesen.csv")

# ---------------------------------------
# Session State
# ---------------------------------------

if "punkte" not in st.session_state:
    st.session_state.punkte = 0
if "gesamt" not in st.session_state:
    st.session_state.gesamt = 0

# ---------------------------------------
# UI
# ---------------------------------------

st.title("🇮🇹 MarleneLingo 6.0 PRO 🚀")
st.write(f"🌟 Punkte: {st.session_state.punkte} / {st.session_state.gesamt}")

modus = st.selectbox("Wähle deinen Lernmodus:", ["Vokabeln", "Grammatik", "Leseverständnis"])

# ---------------------------------------
# Vokabelmodus
# ---------------------------------------

if modus == "Vokabeln":
    level = st.selectbox("Wähle dein Sprachlevel:", vokabeln["level"].unique())
    daten = vokabeln[vokabeln["level"] == level].sample(1).iloc[0]
    richtung = random.choice(["de_it", "it_de"])

    if richtung == "de_it":
        eingabe = st.text_input(f"Wie heißt '{daten['de']}' auf Italienisch?")
        korrekt = daten["it"]
    else:
        eingabe = st.text_input(f"Was bedeutet '{daten['it']}' auf Deutsch?")
        korrekt = daten["de"]

    if eingabe:
    st.session_state.gesamt += 1
    if eingabe.lower() == korrekt.lower():
        st.success("✅ Richtig!")
        st.session_state.punkte += 1
    else:
        st.error(f"❌ Falsch! Richtig wäre: {korrekt}")
    st.experimental_rerun()


# ---------------------------------------
# Grammatikmodus
# ---------------------------------------

elif modus == "Grammatik":
    daten = grammatik.sample(1).iloc[0]
    st.write(daten["frage"])
    antwort = st.radio("Wähle die richtige Form:", [daten["option1"], daten["option2"], daten["option3"]])

   if st.button("Antwort prüfen", key="grammatik"):
    st.session_state.gesamt += 1
    if antwort == daten["antwort"]:
        st.success("✅ Richtig!")
        st.session_state.punkte += 1
    else:
        st.error(f"❌ Falsch! Richtig wäre: {daten['antwort']}")
    st.experimental_rerun()


# ---------------------------------------
# Leseverständnis
# ---------------------------------------

elif modus == "Leseverständnis":
    daten = lesen.sample(1).iloc[0]
    st.write("📖 **Text:**")
    st.write(daten["text"])
    st.write(daten["frage"])
    antwort = st.radio("Wähle:", [daten["option1"], daten["option2"], daten["option3"]])

    if st.button("Antwort prüfen", key="lesen"):
    st.session_state.gesamt += 1
    if antwort == daten["antwort"]:
        st.success("✅ Richtig!")
        st.session_state.punkte += 1
    else:
        st.error(f"❌ Falsch! Richtig wäre: {daten['antwort']}")
    st.experimental_rerun()


# Fortschrittsbalken
if st.session_state.gesamt > 0:
    st.progress(st.session_state.punkte / st.session_state.gesamt)
