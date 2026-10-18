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
FILE_DATI = "storico_28giorni.json"

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
    st.subheader("📋 Ciclo Mensile: 4 Settimane x 7 Giorni")
    st.markdown("Seleziona la settimana e compila i 7 giorni con descrizione, km, tempi, biometria e carichi.")

    # Sotto-menu per scegliere quale settimana visualizzare/compilare
    settimana_scelta = st.selectbox("Seleziona la Settimana da compilare:", ["Settimana 1", "Settimana 2", "Settimana 3", "Settimana 4"])
    
    num_sett = int(settimana_scelta.split(" ")[1])

    st.markdown(f"### 📌 Inserimento Dettagliato - {settimana_scelta}")
    
    km_settimana_tot = 0.0
    minuti_settimana_tot = 0
    carico_settimana_tot = 0.0
    ritmi_settimana = []
    bpm_max_sett = 0
    bpm_min_sett = 999
    cadenze_sett = []

    # 7 Giorni della settimana
    for giorno in range(1, 8):
        with st.expander(f"📅 Giorno {giorno} - {settimana_scelta}", expanded=(giorno == 1)):
            
            descrizione_allenamento = st.text_input(f"Descrizione Allenamento (Giorno {giorno})", key=f"desc_s{num_sett}_g{giorno}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### 📊 Dati Prestazione")
                km_g = st.number_input(f"Distanza (Km) - Giorno {giorno}", min_value=0.0, value=0.0, step=0.1, key=f"km_s{num_sett}_g{giorno}")
                
                gm_min = st.number_input(f"Minuti Impiegati - Giorno {giorno}", min_value=0, max_value=300, value=0, key=f"min_s{num_sett}_g{giorno}")
                ritmo_g = st.selectbox(f"Ritmo al Km - Giorno {giorno}", ritmi_disponibili, key=f"rit_s{num_sett}_g{giorno}")
                
            with c2:
                st.markdown("#### ❤️ Biometria & Carico")
                bpm_max_g = st.number_input(f"BPM Max - Giorno {giorno}", 0, 220, 0, key=f"bmax_s{num_sett}_g{giorno}")
                bpm_min_g = st.number_input(f"BPM Min - Giorno {giorno}", 0, 150, 0, key=f"bmin_s{num_sett}_g{giorno}")
                cad_g = st.number_input(f"Cadenza (spm) - Giorno {giorno}", 0, 220, 0, key=f"cad_s{num_sett}_g{giorno}")
                sforzo_g = st.slider(f"Sforzo (1-10) - Giorno {giorno}", 1, 10, 5, key=f"sf_s{num_sett}_g{giorno}")

            # Calcoli del singolo giorno
            sec_ritmo_g = 0
            if ritmo_g != "Seleziona ritmo...":
                mr, sr = map(int, ritmo_g.split(":"))
                sec_ritmo_g = mr * 60 + sr

            carico_giorno = gm_min * sforzo_g if gm_min > 0 else int(km_g * 10 * sforzo_g)

            # Accumulo totali settimana
            km_settimana_tot += km_g
            minuti_settimana_tot += gm_min
            carico_settimana_tot += carico_giorno
            if sec_ritmo_g > 0:
                ritmi_settimana.append(sec_ritmo_g)
            if bpm_max_g > bpm_max_sett:
                bpm_max_sett = bpm_max_g
            if bpm_min_g > 0 and bpm_min_g < bpm_min_sett:
                bpm_min_sett = bpm_min_g
            if cad_g > 0:
                cadenze_sett.append(cad_g)

            st.info(f"🔹 **Carico Giorno {giorno}:** {carico_giorno} punti")

    # --- RIEPILOGO DELLA SETTIMANA SELEZIONATA ---
    st.markdown("---")
    st.subheader(f"📊 Riepilogo Totale - {settimana_scelta}")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.metric("KM Totali Settimana", f"{km_settimana_tot:.2f} km")
    col_s2.metric("Tempo Totale Settimana", f"{minuti_settimana_tot} minuti")
    
    if ritmi_settimana:
        media_rs = sum(ritmi_settimana) / len(ritmi_settimana)
        str_ritmo_s = f"{int(media_rs // 60)}:{int(media_rs % 60):02d} /km"
    else:
        str_ritmo_s = "--:--"
    col_s3.metric("Ritmo Medio Settimana", str_ritmo_s)

    st.markdown(f"🎯 **Carico Complessivo {settimana_scelta}:** {carico_settimana_tot} punti | 🫀 **BPM Max:** {bpm_max_sett} bpm")

    # Pulsante salvataggio ciclo 28 giorni
    nome_salvataggio = st.text_input("Nome da dare a questo piano di allenamento completo:", key="nome_piano_28g")
    if st.button("💾 Salva il Programma Completo"):
        if nome_salvataggio.strip():
            nuovo_record = {
                "titolo": nome_salvataggio,
                "settimana": settimana_scelta,
                "km_settimana": km_settimana_tot,
                "carico_settimana": carico_settimana_tot,
                "ritmo_medio": str_ritmo_s
            }
            storico.append(nuovo_record)
            salva_dati(storico)
            st.success("✅ Dati della settimana salvati correttamente nell'archivio!")
        else:
            st.error("Inserisci un nome valido prima di salvare.")


# ==============================================================================
# SCHEDA 2: CALCOLO RAPIDO RIPETUTE
# ==============================================================================
with tab_scelta2:
    st.subheader("⚡ Strumenti di Calcolo Rapido")
    st.markdown("Usa questo spazio per calcoli veloci di ritmi e tempi.")
    
    c_t1, c_t2, c_t3 = st.columns(3)
    with c_t1:
        km_test = st.number_input("Distanza (km)", 0.0, 100.0, 10.0, 0.1)
    with c_t2:
        m_test = st.number_input("Minuti", 0, 300, 50)
    with c_t3:
        rit_test = st.selectbox("Ritmo", ritmi_disponibili)
        
    if km_test > 0 and m_test > 0:
        sec_m = (m_test * 60) / km_test
        st.success(f"⚡ Ritmo calcolato: {int(sec_m//60)}:{int(sec_m%60):02d} /km")


# ==============================================================================
# SCHEDA 3: ARCHIVIO SALVATO
# ==============================================================================
with tab_scelta3:
    st.subheader("📂 Archivio Piani Salvati")
    if not storico:
        st.info("Nessun piano salvato al momento.")
    else:
        for idx, item in enumerate(storico):
            with st.expander(f"📌 {item['titolo']} ({item['settimana']})"):
                st.write(f"**KM Totali:** {item['km_settimana']:.2f} km")
                st.write(f"**Carico:** {item['carico_settimana']} punti")
                st.write(f"**Ritmo Medio:** {item['ritmo_medio']}")
                
                if st.button(f"🗑️ Elimina '{item['titolo']}'", key=f"del_{idx}"):
                    storico.pop(idx)
                    salva_dati(storico)
                    st.rerun()
