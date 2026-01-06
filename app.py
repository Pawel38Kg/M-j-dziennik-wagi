import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from PIL import Image

st.set_page_config(page_title="Mój Dziennik Fitness", layout="wide")

# --- KONFIGURACJA UŻYTKOWNIKA ---
st.sidebar.header("Twoje Dane")
imie = st.sidebar.text_input("Imię", "Paweł")
wiek = st.sidebar.number_input("Twój wiek", min_value=1, max_value=120, value=30)
wzrost = st.sidebar.number_input("Twój wzrost (cm)", min_value=100, max_value=250, value=180)

def oblicz_bmi(waga, wzrost_cm):
    return round(waga / ((wzrost_cm/100)**2), 1)

def wiek_metaboliczny(wiek, bmi):
    # Uproszczony wzór: BMI powyżej 25 dodaje lata, poniżej odejmuje
    roznica = (bmi - 22) * 0.5
    return int(wiek + roznica)

# --- BAZA DANYCH ---
DB_FILE = "fitness_data.csv"

def load_data():
    try:
        return pd.read_csv(DB_FILE)
    except:
        return pd.DataFrame(columns=["Data", "Waga", "BMI", "Wiek Met.", "Notatka"])

# --- MENU GŁÓWNE ---
st.title(f"💪 Dziennik Fitness: {imie}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Dodaj nowy pomiar")
    data = st.date_input("Data", datetime.date.today())
    waga = st.number_input("Waga (kg)", min_value=30.0, max_value=200.0, value=85.0, step=0.1)
    notatka = st.text_input("Notatka (np. po treningu)")
    foto = st.file_uploader("Dodaj zdjęcie sylwetki", type=['jpg', 'png', 'jpeg'])
    
    if st.button("Zapisz pomiar"):
        df = load_data()
        bmi_akt = oblicz_bmi(waga, wzrost)
        wiek_met = wiek_metaboliczny(wiek, bmi_akt)
        
        nowy_wpis = pd.DataFrame([[data, waga, bmi_akt, wiek_met, notatka]], 
                                columns=["Data", "Waga", "BMI", "Wiek Met.", "Notatka"])
        df = pd.concat([df, nowy_wpis], ignore_index=True)
        df.to_csv(DB_FILE, index=False)
        st.success("Dane zapisane!")

with col2:
    df = load_data()
    if not df.empty:
        ostatnia_waga = df.iloc[-1]['Waga']
        st.metric("Aktualna Waga", f"{ostatnia_waga} kg")
        st.metric("Twoje BMI", df.iloc[-1]['BMI'])
        st.metric("Wiek Metaboliczny", f"{df.iloc[-1]['Wiek Met.']} lat")

st.divider()
if not df.empty:
    st.subheader("Twoje postępy")
    fig = px.line(df, x="Data", y="Waga", title="Zmiana wagi w czasie", markers=True)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Historia pomiarów")
    st.write(df)

