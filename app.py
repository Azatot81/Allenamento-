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
</style>
"""

st.markdown(sfondo_css, unsafe_allow_html=True)

st.title("Dashboard Allenamento (28 Giorni)")

if "autenticato" not in st.session_state:
    st.session_state.autenticato = False

if not st.session_state.autenticato:
    st.subheader("Accesso Riservato")
    password_inserita = st.text_input("Inserisci la password:", type="password", key="pass_login")
    if st.button("Accedi", key="btn_login"):
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

tab1, tab2, tab3 = st.tabs(["Gestione 4 Settimane", "Tabella & PDF", "Archivio & Backup"])

ritmi_disponibili = ["Seleziona ritmo..."]
for m in range(2, 7):
    for s in range(0, 60, 5):
        if (m == 2 and s >= 10) or (m > 2 and m < 6) or (m == 6 and s <= 15):
            ritmi_disponibili.append(str(m) + ":" + f"{s:02d}")

with tab1:
    st.subheader("Ciclo Mensile: 4 Settimane x 7 Giorni")
    
    titolo_predefinito = ""
    if st.session_state.edit_data is not None:
        titolo_predefinito = st.session_state.edit_data.get("titolo", "")
        st.info("Modifica piano: " + titolo_predefinito)

    settimana_scelta = st.selectbox("Seleziona la Settimana:", ["Settimana 1", "Settimana 2", "Settimana 3", "Settimana 4"], key="sel_sett")
    num_sett = int(settimana_scelta.split(" ")[1])

    km_sett_tot = 0.0
    min_sett_tot = 0
    carico_prev_tot = 0.0
    carico_eff_tot = 0.0
    ritmi_sett = []
    bpm_max_sett = 0

    for giorno in range(1, 8):
        s_n = str(num_sett)
        g_n = str(giorno)
        k_p = "p_km_s" + s_n + "_g" + g_n
        k_e = "e_km_s" + s_n + "_g" + g_n
        m_p = "p_min_s" + s_n + "_g" + g_n
        m_e = "e_min_s" + s_n + "_g" + g_n
        s_p = "p_sf_s" + s_n + "_g" + g_n
        s_e = "e_sf_s" + s_n + "_g" + g_n
        r_p_key = "rit_p_s" + s_n + "_g" + g_n
        r_key = "rit_s" + s_n + "_g" + g_n
        rc_key = "rit_calc_s" + s_n + "_g" + g_n
        rc_p_key = "rit_p_calc_s" + s_n + "_g" + g_n
        bmax_k = "bmax_s" + s_n + "_g" + g_n
        bmin_k = "bmin_min_s" + s_n + "_g" + g_n
        cad_k = "cad_s" + s_n + "_g" + g_n
        desc_k = "desc_s" + s_n + "_g" + g_n

        with st.expander("Giorno " + str(giorno) + " - " + settimana_scelta, expanded=(giorno == 1)):
            st.text_input("Descrizione Giorno " + str(giorno), key=desc_k)
            
            st.markdown("### Previsto")
            km_prev = st.number_input("Km Previsti G" + str(giorno), min_value=0.0, value=0.0, step=0.1, key=k_p)
            min_prev = st.number_input("Minuti Previsti G" + str(giorno), min_value=0, max_value=300, value=0, key=m_p)
            st.selectbox("Ritmo Previsto G" + str(giorno), ritmi_disponibili, key=r_p_key)
            st.text_input("Ritmo previsto manuale G" + str(giorno), key=rc_p_key)
            sf_prev = st.selectbox("Sforzo P G" + str(giorno), list(range(1, 11)), index=4, key=s_p)
            
            st.markdown("---")
            st.markdown("### Effettivo")
            km_eff = st.number_input("Km Effettivi G" + str(giorno), min_value=0.0, value=0.0, step=0.1, key=k_e)
            min_eff = st.number_input("Minuti Effettivi G" + str(giorno), min_value=0, max_value=300, value
