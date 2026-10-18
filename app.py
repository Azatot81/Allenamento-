import streamlit as st
import json
import os

st.set_page_config(page_title="Tool Allenamento 4 Settimane - 28 Giorni", layout="wide")

# --- SFONDO PERSONALIZZATO ---
sfondo_css = """
<style>
.stApp {
background-image:
url("https://www.liceodonmilani.it/wp-content/uploads/2021/06/Schermata-2018-01-22-alle-12.49.06-980x490-1.png");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
}
</style>
"""
st.markdown(sfondo_css, unsafe_allow_html=True)

# --- 1. PROTEZIONE PASSWORD ---
st.sidebar.header("Accesso Riservato")
password_inserita = st.sidebar.text_input("Inserisci la password:", type="password")
if password_inserita != "allenamento2026":
    st.warning("⚠️ Inserisci la password corretta nella barra laterale per sbloccare l'applicazione.")
    st.stop()
st.sidebar.success("Accesso Autorizzato!")

st.title("🏃‍♂️ Programmazione 4 Settimane (28 Giorni di Allenamento)")

# --- GESTIONE ARCHIVIO DATI (SALVATAGGIO) ---
FILE_DATI = "storico_28giorni_carichi.json"

def carica_dati():
    if os.path.exists(FILE_DATI):
        with open(FILE_DATI, "r") as f:
            return json.load(f)
    return []

def salva_dati(dati):
    with open(FILE_DATI, "w") as f:
        json.dump(dati, f)

storico = carica_dati()

# --- MENU A SCHEDE PRINCIPALE ---
tab_scelta1, tab_scelta2, tab_scelta3 = st.tabs([
    "📅 Gestione 4 Settimane (7 Giorni x Settimana)", 
    "⚡ Calcolo Rapido Ripetute", 
    "📂 Archivio Cicli Salvati"
])

# Lista ritmi a tendina
ritmi_disponibili = ["Seleziona ritmo..."]
for m in range(2, 7):
    for s in range(0, 60, 5):
        if (m == 2 and s >= 10) or (m > 2 and m < 6) or (m == 6 and s <= 15):
            ritmi_disponibili.append(f"{m}:{s:02d}")

# ==============================================================================
# SCHEDA 1: PROGRAMMAZIONE 4 SETTIMANE CON 7 GIORNI CIASCUNA
# ==============================================================================
with tab_scelta1:
    st.subheader("📋 Ciclo Mensile: 4 Settimane x 7 Giorni (Previsto vs Effettivo & Carichi)")
    st.markdown("Seleziona la settimana e compila i 7 giorni con descrizioni, km, tempi, biometria e calcolo dei carichi.")

    # Sotto-menu per scegliere quale settimana visualizzare/compilare
    settimana_scelta = st.selectbox("Seleziona la Settimana da compilare:", ["Settimana 1", "Settimana 2", "Settimana 3", "Settimana 4"])
    
    num_sett = int(settimana_scelta.split(" ")[1])

    st.markdown(f"### 📌 Inserimento Dettagliato - {settimana_scelta}")
    
    km_settimana_tot = 0.0
    minuti_settimana_tot = 0
    carico_prev_sett_tot = 0.0
    carico_eff_sett_tot = 0.0
    ritmi_settimana = []
    bpm_max_sett = 0
    bpm_min_sett = 999

    # 7 Giorni della settimana
    for giorno in range(1, 8):
        with st.expander(f"📅 Giorno {giorno} - {settimana_scelta}", expanded=(giorno == 1)):
            
            descrizione_allenamento = st.text_input(f"Descrizione Allenamento (Giorno {giorno})", key=f"desc_s{num_sett}_g{giorno}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### 📋 Previsto")
                km_g_prev = st.number_input(f"Km Previsti - Giorno {giorno}", min_value=0.0, value=0.0, step=0.1, key=f"km_p_s{num_sett}_g{g
