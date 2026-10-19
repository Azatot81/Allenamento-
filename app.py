import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="Tool Allenamento - 28 Giorni", layout="wide")

# --- CSS PERSONALIZZATO PER CONTRASTO E STILE TABELLA EXCEL ---
sfondo_css = """
<style>
.stApp {
background-image: url("https://www.liceodonmilani.it/wp-content/uploads/2021/06/Schermata-2018-01-22-alle-12.49.06-980x490-1.png");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 95% !important;
}
div.stExpander, div.stTabs [data-baseweb="tab-panel"], section[data-testid="stSidebar"], div[data-testid="stVerticalBlock"] > div {
    background-color: rgba(255, 255, 255, 0.96) !important;
    border-radius: 10px;
    padding: 12px;
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

st.title("🏃‍♂️ Dashboard Allenamento (28 Giorni)")

# --- LOGIN ---
if "autenticato" not in st.session_state:
    st.session_state.autenticato = False

if not st.session_state.autenticato:
    st.subheader("🔒 Accesso Riservato")
    password_inserita = st.text_input("Inserisci la password per sbloccare l'app:", type="password", key="pass_input")
    if st.button("Accedi"):
        if password_inserita == "allenamento2026":
            st.session_state.autenticato = True
            st.rerun()
        else:
            st.error("⚠️ Password errata!")
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

tab_scelta1, tab_scelta2, tab_scelta3 = st.tabs([
    "📅 Gestione 4 Settimane (28 Giorni)", 
    "📊 Schema Tabulare & Stampa PDF",
    "📂 Archivio, Modifica & Backup"
])

ritmi_disponibili = ["Seleziona ritmo..."]
for m in range(2, 7):
    for s in range(0, 60, 5):
        if (m == 2 and s >= 10) or (m > 2 and m < 6) or (m == 6 and s <= 15):
            ritmi_disponibili.append(f"{m}:{s:02d}")

def mostra_banner_sforzo(valore):
    colori_sforzo = {
        1: "🟢 Molto Leggero (Rigenerante)",
        2: "🟢 Leggero (Corsa lenta)",
        3: "🔵 Moderato (Fondo lungo)",
        4: "🔵 Medio-Basso (Progressivo)",
        5: "🟡 Medio (Ritmo medio)",
        6: "🟡 Impegnativo (Soglia)",
        7: "🟠 Forte (Corto veloce)",
        8: "🔴 Molto Forte (Ripetute brevi)",
        9: "🔴 Estenuante (Massima potenza)",
        10: "🔥 Massimale (Gara)"
    }
    desc = colori_sforzo.get(valore, "Normale")
    st.markdown(f'<div style="background-color: #fff3cd; color: #000000; padding: 8px; border-radius: 6px; text-align: center; font-weight: bold; margin-bottom: 10px; font-size: 14px; border: 1px solid #ffeeba;">🟡 Sforzo {valore}: {desc}</div>', unsafe_allow_html=True)

with tab_scelta1:
    st.subheader("📋 Ciclo Mensile: 4 Settimane x 7 Giorni")
    
    titolo_predefinito = ""
    if st.session_state.edit_data:
        titolo_predefinito = st.session_state.edit_data.get("titolo", "")
        st.info(f"✏️ Stai modificando il piano: **{titolo_predefinito}**")

    settimana_scelta = st.selectbox("Seleziona la Settimana:", ["Settimana 1", "Settimana 2", "Settimana 3", "Settimana 4"])
    num_sett = int(settimana_scelta.split(" ")[1])

    km_sett_tot = 0.0
    min_sett_tot = 0
    carico_prev_tot = 0.0
    carico_eff_tot = 0.0
    ritmi_sett = []
    bpm_max_sett = 0
    bpm_min_sett = 999

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
        bmin_k = "bmin_s" + s_n + "_g" + g_n
        cad_k = "cad_s" + s_n + "_g" + g_n
        desc_k = "desc_s" + s_n + "_g" + g_n

        with st.expander(f"📅 Giorno {giorno} - Settimana {num_sett}", expanded=(giorno == 1)):
            st.text_input("Descrizione Allenamento", key=desc_k)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("#### 📋 Previsto")
                km_prev = st.number_input("Km Previsti", min_value=0.0, value=0.0, step=0.1, key=k_p)
                min_prev = st.number_input("Minuti Previsti", min_value=0, max_value=300, value=0, key=m_p)
                rit_prev = st.selectbox("Ritmo Previsto", ritmi_disponibili, key=r_p_key)
                
                r_prev_auto = "--:--"
                if km_prev > 0 and min_prev > 0:
                    sec_p_auto = (min_prev * 60) / km_prev
                    r_prev_auto = f"{int(sec_p_auto // 60)}:{int(sec_p_auto % 60):02d}"
                
                st.markdown(f"⚡ **Ritmo Previsto Calcolato:** `{r_prev_auto} /km`")
                st.text_input("Oppure ritmo previsto manuale:", key=rc_p_key)

                st.markdown("**Sforzo Previsto (1-10)**")
                sf_prev = st.selectbox("", list(range(1, 11)), index=4, key=s_p)
                mostra_banner_sforzo(sf_prev)
                
            with c2:
                st.markdown("#### ✅ Effettivo")
                km_eff = st.number_input("Km Effettivi", min_value=0.0, value=0.0, step=0.1, key=k_e)
                min_eff = st.number_input("Minuti Effettivi", min_value=0, max_value=300, value=0, key=m_e)
                rit_eff = st.selectbox("Ritmo Effettivo", ritmi_disponibili, key=r_key)
                
                ritmo_calcolato_auto = "--:--"
                if km_eff > 0 and min_eff > 0:
                    sec_tot_calc = (min_eff * 60) / km_eff
                    m_calc = int(sec_tot_calc // 60)
                    s_calc = int(sec_tot_calc % 60)
                    ritmo_calcolato_auto = f"{m_calc}:{s_calc:02d}"

                st.markdown(f"⚡ **Ritmo Effettivo Calcolato:** `{ritmo_calcolato_auto} /km`")
                ritmo_inserito_utente = st.text_input("Oppure ritmo effettivo manuale (es. 4:30):", key=rc_key)

                st.markdown("**Sforzo Effettivo (1-10)**")
                sf_eff = st.selectbox("", list(range(1, 11)), index=4, key=s_e)
                mostra_banner_sforzo(sf_eff)
                
            with c3:
                st.markdown("#### ❤️ Biometria")
                b_max = st.number_input("BPM Max", 0, 220, 0, key=bmax_k)
                b_min = st.number
