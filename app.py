import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="Tool Allenamento - 28 Giorni", layout="wide")

sfondo_css = """
<style>
.stApp {
background-image: url("https://www.liceodonmilani.it/wp-content/uploads/2021/06/Schermata-2018-01-22-alle-12.49.06-980x490-1.png");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 3rem;
    max-width: 95% !important;
}
div.stExpander, div.stTabs [data-baseweb="tab-panel"], section[data-testid="stSidebar"], div[data-testid="stVerticalBlock"] > div {
    background-color: rgba(255, 255, 255, 0.98) !important;
    border-radius: 10px;
    padding: 15px;
    color: #000000 !important;
}
h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: #111111 !important;
}
input, select, textarea, div[data-baseweb="select"] > div, [data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"] {
    background-color: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}
[role="option"] div, [role="option"] span {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}
button, button p, div[data-testid="stButton"] > button {
    background-color: #d9534f !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-weight: bold !important;
    border-radius: 8px !important;
    border: none !important;
}
button[aria-label="Show password"], button[aria-label="Hide password"] {
    background-color: #e9ecef !important;
    color: #000000 !important;
}
</style>
"""
st.markdown(sfondo_css, unsafe_allow_html=True)

st.title("Dashboard Allenamento (28 Giorni)")

if "autenticato" not in st.session_state:
    st.session_state.autenticato = False

if not st.session_state.autenticato:
    st.subheader("Accesso Riservato")
    password_inserita = st.text_input("Inserisci la password per sbloccare l'app:", type="password", key="pass_input_login")
    if st.button("Accedi", key="btn_login_submit"):
        if password_inserita == "allenamento2026":
            st.session_state.autenticato = True
            st.rerun()
        else:
            st.error("Password errata!")
    st.stop()

FILE_DATI = "storico_28giorni_carichi.json"

def carica_dati():
    if os.path.exists(FILE_DATI):
        try:
            with open(FILE_DATI, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def salva_dati(dati):
    with open(FILE_DATI, "w") as f:
        json.dump(dati, f)

storico = carica_dati()

if "edit_data" not in st.session_state:
    st.session_state.edit_data = None

tab_scelta1, tab_scelta2, tab_scelta3 = st.tabs(
