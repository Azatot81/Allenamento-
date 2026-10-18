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

    settimana_scelta = st.selectbox("Seleziona la Settimana da compilare:", ["Settimana 1", "Settimana 2", "Settimana 3", "Settimana 4"])
    
    num_sett = int(settimana_scelta.split(" ")[1])

    st.markdown(f"### 📌 Inserimento Dettagliato - Settimana {num_sett}")
    
    km_settimana_tot = 0.0
    minuti_settimana_tot = 0
    carico_prev_sett_tot = 0.0
    carico_eff_sett_tot = 0.0
    ritmi_settimana = []
    bpm_max_sett = 0
    bpm_min_sett = 999

    # 7 Giorni della settimana
    for giorno in range(1, 8):
        k_p = f"p_km_s{num_sett}_g{giorno}"
        k_e = f"e_km_s{num_sett}_g{giorno}"
        m_p = f"p_min_s{num_sett}_g{giorno}"
        m_e = f"e_min_s{num_sett}_g{giorno}"
        s_p = f"p_sf_s{num_sett}_g{giorno}"
        s_e = f"e_sf_s{num_sett}_g{giorno}"
        r_key = f"rit_s{num_sett}_g{giorno}"
        bmax_k = f"bmax_s{num_sett}_g{giorno}"
        bmin_k = f"bmin_s{num_sett}_g{giorno}"
        cad_k = f"cad_s{num_sett}_g{giorno}"
        desc_k = f"desc_s{num_sett}_g{giorno}"

        with st.expander(f"📅 Giorno {giorno} - Settimana {num_sett}", expanded=(giorno == 1)):
            
            descrizione_allenamento = st.text_input("Descrizione Allenamento", key=desc_k)
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### 📋 Previsto")
                km_g_prev = st.number_input("Km Previsti", min_value=0.0, value=0.0, step=0.1, key=k_p)
                min_g_prev = st.number_input("Minuti Previsti", min_value=0, max_value=300, value=0, key=m_p)
                sforzo_prev = st.slider("Sforzo Previsto (1-10)", 1, 10, 5, key=s_p)
                
            with c2:
                st.markdown("#### ✅ Effettivo & Biometria")
                km_g_eff = st.number_input("Km Effettivi", min_value=0.0, value=0.0, step=0.1, key=k_e)
                min_g_eff = st.number_input("Minuti Effettivi", min_value=0, max_value=300, value=0, key=m_e)
                ritmo_g = st.selectbox("Ritmo Effettivo al Km", ritmi_disponibili, key=r_key)
                sforzo_eff = st.slider("Sforzo Effettivo (1-10)", 1, 10, 5, key=s_e)
                
                bpm_max_g = st.number_input("BPM Max", 0, 220, 0, key=bmax_k)
                bpm_min_g = st.number_input("BPM Min", 0, 150, 0, key=bmin_k)
                cad_g = st.number_input("Cadenza (spm)", 0, 220, 0, key=cad_k)

            carico_prev_giorno = min_g_prev * sforzo_prev if min_g_prev > 0 else int(km_g_prev * 10 * sforzo_prev)
            carico_eff_giorno = min_g_eff * sforzo_eff if min_g_eff > 0 else int(km_g_eff * 10 * sforzo_eff)

            sec_ritmo_g = 0
            if ritmo_g != "Seleziona ritmo...":
                mr, sr = map(int, ritmo_g.split(":"))
                sec_ritmo_g = mr * 60 + sr

            km_settimana_tot += km_g_eff
            minuti_settimana_tot += min_g_eff
            carico_prev_sett_tot += carico_prev_giorno
            carico_eff_sett_tot += carico_eff_giorno
            
            if sec_ritmo_g > 0:
                ritmi_settimana.append(sec_ritmo_g)
            if bpm_max_g > bpm_max_sett:
                bpm_max_sett = bpm_max_g
            if bpm_min_g > 0 and bpm_min_g < bpm_min_sett:
                bpm_min_sett = bpm_min_g

            st.info(f"🔹 Carico Previsto Giorno {giorno}: {carico_prev_giorno} | 🔸 Carico Effettivo Giorno {giorno}: {carico_eff_giorno}")

    # --- RIEPILOGO DELLA SETTIMANA SELEZIONATA ---
    st.markdown("---")
    st.subheader(f"📊 Riepilogo Totale - Settimana {num_sett}")
    
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    col_s1.metric("KM Totali Effettivi", f"{km_settimana_tot:.2f} km")
    col_s2.metric("Carico Previsto Totale", f"{carico_prev_sett_tot} pt")
    col_s3.metric("Carico Effettivo Totale", f"{carico_eff_sett_tot} pt")
    
    if ritmi_settimana:
        media_rs = sum(ritmi_settimana) / len(ritmi_settimana)
        str_ritmo_s = f"{int(media_rs // 60)}:{int(media_rs % 60):02d} /km"
    else:
        str_ritmo_s = "--:--"
    col_s4.metric("Ritmo Medio Settimana", str_ritmo_s)

    st.markdown(f"🫀 **BPM Max Settimana:** {bpm_max_sett} bpm")

    nome_salvataggio = st.text_input("Nome da dare a questo piano di allenamento:", key="nome_piano_28g")
    if st.button("💾 Salva il Programma della Settimana"):
        if nome_salvataggio.strip():
            nuovo_record = {
                "titolo": nome_salvataggio,
                "settimana": settimana_scelta,
                "km_settimana": km_settimana_tot,
                "carico_previsto": carico_prev_sett_tot,
                "carico_effettivo": carico_eff_sett_tot,
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
                st.write(f"**Carico Previsto:** {item['carico_previsto']} pt | **Carico Effettivo:** {item['carico_effettivo']} pt")
                st.write(f"**Ritmo Medio:** {item['ritmo_medio']}")
                
                if st.button(f"🗑️ Elimina '{item['titolo']}'", key=f"del_{idx}"):
                    storico.pop(idx)
                    salva_dati(storico)
                    st.rerun()
