import streamlit as st
import json
import os

st.set_page_config(page_title="Tool Allenamento Tablet - 28 Giorni", layout="wide")

# --- CSS PERSONALIZZATO PER TABLET / ORIZZONTALE ---
sfondo_css = """
<style>
.stApp {
background-image:
url("https://www.liceodonmilani.it/wp-content/uploads/2021/06/Schermata-2018-01-22-alle-12.49.06-980x490-1.png");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
}
/* Ottimizzazione tabelle e spazi per tablet orizzontale */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 95% !important;
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

st.title("🏃‍♂️ Dashboard Allenamento - Vista Tablet (28 Giorni)")

# --- GESTIONE ARCHIVIO DATI ---
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
    "📅 Gestione 4 Settimane (Tablet View)", 
    "⚡ Calcolo Rapido Ripetute", 
    "📂 Archivio Cicli Salvati"
])

# Lista ritmi a tendina
ritmi_disponibili = ["Seleziona ritmo..."]
for m in range(2, 7):
    for s in range(0, 60, 5):
        if (m == 2 and s >= 10) or (m > 2 and m < 6) or (m == 6 and s <= 15):
            ritmi_disponibili.append(f"{m}:{s:02d}")

# Funzione per generare il banner dinamico dello sforzo
def mostra_banner_sforzo(valore_sforzo, prefisso_chiave):
    colori = {
        1: ("#d4edda", "#155724", "🟢 Molto Leggero (Recupero attivo / Rigenerante)"),
        2: ("#d4edda", "#155724", "🟢 Leggero (Corsa lenta / Fondo base)"),
        3: ("#d1ecf1", "#0c5460", "🔵 Moderato (Fondo lungo / Ritmo respirabile)"),
        4: ("#d1ecf1", "#0c5460", "🔵 Medio-Basso (Corsa progressiva iniziale)"),
        5: ("#fff3cd", "#856404", "🟡 Medio (Ritmo medio / Fondo ritmato)"),
        6: ("#fff3cd", "#856404", "🟡 Impegnativo (Soglia anaerobica / Fartlek)"),
        7: ("#ffeeba", "#856404", "🟠 Forte (Ripetute medie / Corto veloce)"),
        8: ("#f8d7da", "#721c24", "🔴 Molto Forte (Ripetute brevi / Fuori soglia)"),
        9: ("#f5c6cb", "#721c24", "🔴 Estenuante (Massima potenza aerobica)"),
        10: ("#dc3545", "#ffffff", "🔥 Massimale (Sforzo totale / Gara)")
    }
    bg, fg, testo = colori.get(valore_sforzo, ("#e2e3e5", "#383d41", "Neutro"))
    html_banner = f"""
    <div style="background-color: {bg}; color: {fg}; padding: 8px 12px; border-radius: 6px; text-align: center; font-weight: bold; margin-top: 5px; margin-bottom: 10px; font-size: 14px;">
        {testo}
    </div>
    """
    st.markdown(html_banner, unsafe_allow_html=True)

# ==============================================================================
# SCHEDA 1: PROGRAMMAZIONE 4 SETTIMANE CON 7 GIORNI (ORIZZONTALE TABLET)
# ==============================================================================
with tab_scelta1:
    st.subheader("📋 Ciclo Mensile: 4 Settimane x 7 Giorni")
    
    settimana_scelta = st.selectbox("Seleziona la Settimana da compilare:", ["Settimana 1", "Settimana 2", "Settimana 3", "Settimana 4"])
    num_sett = int(settimana_scelta.split(" ")[1])

    km_settimana_tot = 0.0
    minuti_settimana_tot = 0
    carico_prev_sett_tot = 0.0
    carico_eff_sett_tot = 0.0
    ritmi_settimana = []
    bpm_max_sett = 0
    bpm_min_sett = 999

    # 7 Giorni della settimana ottimizzati per schermo orizzontale
    for giorno in range(1, 8):
        k_p = f"p_km_s{num_sett}_g{giorno}"
        k_e = f"e_km_s{num_sett}_g{giorno}"
        m_p = f"p_min_s{num_sett}_g{giorno}"
        m_e = f"e_min_s{num_sett}_g{giorno}"
        s_p = f"p_sf_
