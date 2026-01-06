import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

st.set_page_config(page_title="Mój Dziennik Wagi", page_icon="⚖️")

st.title("⚖️ Dziennik Odchudzania")

# Prosta baza danych w pliku CSV
DB_FILE = "waga_data.csv"

def load_data():
    try:
        return pd.read_csv(DB_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Data", "Waga", "Tkanka_Tluszczowa", "Miesnie", "BMI"])

data = load_data()

# Formularz dodawania pomiaru
with st.expander("➕ Dodaj nowy pomiar", expanded=True):
    with st.form("weight_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Data", datetime.date.today())
            weight = st.number_input("Waga (kg)", min_value=30.0, max_value=200.0, step=0.1)
        with col2:
            fat = st.number_input("Tkanka tłuszczowa (%)", min_value=1.0, max_value=60.0, step=0.1)
            muscle = st.number_input("Masa mięśniowa (kg)", min_value=10.0, max_value=150.0, step=0.1)
        
        submit = st.form_submit_button("Zapisz pomiar")
        
        if submit:
            new_entry = pd.DataFrame([[date, weight, fat, muscle, round(weight / (1.8**2), 2)]], 
                                     columns=data.columns)
            data = pd.concat([data, new_entry], ignore_index=True)
            data.to_csv(DB_FILE, index=False)
            st.success("Zapisano!")

# Wyświetlanie statystyk
if not data.empty:
    st.subheader("Twój postęp")
    
    # Wykres
    fig = px.line(data, x="Data", y="Waga", title="Zmiana wagi w czasie", markers=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela z historią
    st.subheader("Historia pomiarów")
    st.dataframe(data.sort_values(by="Data", ascending=False), use_container_width=True)
    
    # Przycisk eksportu (np. do Excela)
    st.download_button("Pobierz dane jako CSV", data.to_csv(index=False), "moja_waga.csv", "text/csv")
else:
    st.info("Dodaj pierwszy pomiar, aby zobaczyć wykres!")
