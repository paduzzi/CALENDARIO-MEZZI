import streamlit as st
import pandas as pd
import datetime

# Caricamento dati mezzi dal file Excel
@st.cache_data
def load_mezzi():
    df = pd.read_excel("Automezzi ASP (8).xlsx", skiprows=1)  # Saltiamo la prima riga doppia intestazione
    return df

mezzi = load_mezzi()

st.title("🚐 Calendario prenotazioni automezzi")

# Selezione mezzo (usiamo il MODELLO come identificativo)
mezzo = st.selectbox("Seleziona un mezzo", mezzi["MODELLO"].dropna().unique())

# Carica prenotazioni esistenti
try:
    prenotazioni = pd.read_csv("prenotazioni.csv")
except FileNotFoundError:
    prenotazioni = pd.DataFrame(columns=["Modello", "Data", "Ora Inizio", "Ora Fine", "Utente"])

# Mostra prenotazioni già fatte
st.subheader(f"📅 Prenotazioni per {mezzo}")
st.table(prenotazioni[prenotazioni["Modello"] == mezzo])

# Form prenotazione
st.subheader("➕ Nuova prenotazione")
with st.form("nuova_prenotazione"):
    data = st.date_input("Data", datetime.date.today())
    ora_inizio = st.time_input("Ora inizio", datetime.time(9, 0))
    ora_fine = st.time_input("Ora fine", datetime.time(17, 0))
    utente = st.text_input("Nome utente")
    submit = st.form_submit_button("Prenota")

if submit:
    nuova = pd.DataFrame([[mezzo, data, ora_inizio, ora_fine, utente]],
                         columns=["Modello", "Data", "Ora Inizio", "Ora Fine", "Utente"])
    prenotazioni = pd.concat([prenotazioni, nuova], ignore_index=True)
    prenotazioni.to_csv("prenotazioni.csv", index=False)
    st.success("✅ Prenotazione registrata!")
