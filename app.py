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
        desc_k = "desc_s" + s_n + "_g" + g_n

        with st.expander("Giorno " + str(giorno) + " - " + settimana_scelta, expanded=(giorno == 1)):
            st.text_input("Descrizione Giorno " + str(giorno), key=desc_k)
            
            st.markdown("Previsto")
            km_prev = st.number_input("Km Previsti G" + str(giorno), min_value=0.0, value=0.0, step=0.1, key=k_p)
            min_prev = st.number_input("Minuti Previsti G" + str(giorno), min_value=0, max_value=300, value=0, key=m_p)
            st.selectbox("Ritmo Previsto G" + str(giorno), ritmi_disponibili, key=r_p_key)
            st.text_input("Ritmo previsto manuale G" + str(giorno), key=rc_p_key)
            sf_prev = st.selectbox("Sforzo P G" + str(giorno), list(range(1, 11)), index=4, key=s_p)
            
            st.markdown("---")
            st.markdown("Effettivo")
            km_eff = st.number_input("Km Effettivi G" + str(giorno), min_value=0.0, value=0.0, step=0.1, key=k_e)
            min_eff = st.number_input("Minuti Effettivi G" + str(giorno), min_value=0, max_value=300, value=0, key=m_e)
            rit_eff = st.selectbox("Ritmo Effettivo G" + str(giorno), ritmi_disponibili, key=r_key)
            ritmo_inserito_utente = st.text_input("Ritmo effettivo manuale G" + str(giorno), key=rc_key)
            sf_eff = st.selectbox("Sforzo E G" + str(giorno), list(range(1, 11)), index=4, key=s_e)
            
            st.markdown("---")
            b_max = st.number_input("BPM Max G" + str(giorno), 0, 220, 0, key=bmax_k)

            c_prev = min_prev * sf_prev if min_prev > 0 else int(km_prev * 10 * sf_prev)
            c_eff = min_eff * sf_eff if min_eff > 0 else int(km_eff * 10 * sf_eff)

            ritmo_finale_scelto = ritmo_inserito_utente.strip() if ritmo_inserito_utente.strip() else rit_eff
            
            sec_r = 0
            if ritmo_finale_scelto != "Seleziona ritmo..." and ":" in ritmo_finale_scelto:
                try:
                    mr, sr = map(int, ritmo_finale_scelto.split(":"))
                    sec_r = mr * 60 + sr
                except:
                    sec_r = 0

            km_sett_tot += km_eff
            min_sett_tot += min_eff
            carico_prev_tot += c_prev
            carico_eff_tot += c_eff
            
            if sec_r > 0:
                ritmi_sett.append(sec_r)
            if b_max > bpm_max_sett:
                bpm_max_sett = b_max

            st.info("Carico Previsto: " + str(c_prev) + " pt | Carico Effettivo: " + str(c_eff) + " pt")

    st.markdown("---")
    st.subheader("Riepilogo - " + settimana_scelta)
    
    cs1, cs2, cs3, cs4 = st.columns(4)
    cs1.metric("KM Totali", f"{km_sett_tot:.2f} km")
    cs2.metric("Carico Previsto", str(carico_prev_tot) + " pt")
    cs3.metric("Carico Effettivo", str(carico_eff_tot) + " pt")
    
    if ritmi_sett:
        m_rs = sum(ritmi_sett) / len(ritmi_sett)
        str_r = str(int(m_rs // 60)) + ":" + f"{int(m_rs % 60):02d}" + " /km"
    else:
        str_r = "--:--"
    cs4.metric("Ritmo Medio", str_r)

    nome_salv = st.text_input("Nome piano:", value=titolo_predefinito, key="nome_piano_in")
    if st.button("Salva Settimana", key="btn_salva"):
        if nome_salv.strip():
            nuovo_record = {
                "titolo": nome_salv,
                "settimana": settimana_scelta,
                "km_settimana": km_sett_tot,
                "carico_previsto": carico_prev_tot,
                "carico_effettivo": carico_eff_tot,
                "ritmo_medio": str_r
            }
            storico.append(nuovo_record)
            salva_dati(storico)
            st.success("Salvato!")
            st.session_state.edit_data = None
            st.rerun()
        else:
            st.error("Inserisci un nome.")

with tab2:
    st.subheader("Schema Tabulare & Stampa PDF")
    sett_tabella = st.selectbox("Seleziona Settimana Tabella:", ["Settimana 1", "Settimana 2", "Settimana 3", "Settimana 4"], key="tab_rep")
    n_s_tab = int(sett_tabella.split(" ")[1])

    dati_tabella = []
    for g in range(1, 8):
        s_n = str(n_s_tab)
        g_n = str(g)
        desc = st.session_state.get("desc_s" + s_n + "_g" + g_n, "Allenamento " + str(g))
        k_prev = st.session_state.get("p_km_s" + s_n + "_g" + g_n, 0.
