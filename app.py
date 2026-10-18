import streamlit as st
import json
import os

st.set_page_config(page_title="Tool Allenamento Corsi - 4 Settimane", layout="wide")

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

st.title("🏃‍♂️ Dashboard Avanzata - 4 Settimane & Biometria")

# --- GESTIONE ARCHIVIO DATI (SALVATAGGIO) ---
FILE_DATI = "storico_allenamenti_4sett.json"

def carica_dati():
    if os.path.exists(FILE_DATI):
        with open(FILE_DATI, "r") as f:
            return json.load(f)
    return []

def salva_dati(dati):
    with open(FILE_DATI, "w") as f:
        json.dump(dati, f)

storico = carica_dati()

# --- MENU A SCHEDE ---
tab_scelta1, tab_scelta2, tab_scelta3 = st.tabs([
    "📅 Programmazione 4 Settimane & Biometria", 
    "⚡ Calcolo Rapido & Ripetute", 
    "📂 Storico Salvato"
])

# Generiamo la lista dei ritmi a tendina da 2:10 a 6:15 ogni 5 secondi
ritmi_disponibili = ["Seleziona ritmo..."]
for m in range(2, 7):
    for s in range(0, 60, 5):
        if (m == 2 and s >= 10) or (m > 2 and m < 6) or (m == 6 and s <= 15):
            ritmi_disponibili.append(f"{m}:{s:02d}")


# ==============================================================================
# SCHEDA 1: PROGRAMMAZIONE 4 SETTIMANE + BIOMETRIA & CARICHI
# ==============================================================================
with tab_scelta1:
    st.subheader("📈 Ciclo Completo su 4 Settimane")
    st.markdown("Inserisci i dati previsti/effettivi, i carichi, i battiti (max/min con minutaggio) e la cadenza per ciascuna settimana.")

    km_totali_4s = 0.0
    secondi_totali_4s = 0
    ritmi_validi_4s = []
    carico_tot_4s = 0.0
    
    # Liste per calcolare i record biometrici globali
    tutti_bpm_max = []
    tutti_bpm_min = []
    tutte_cadenze = []

    # Creiamo un blocco per ciascuna delle 4 settimane
    for settimana in range(1, 5):
        with st.expander(f"📌 SETTIMANA {settimana}", expanded=(settimana == 1)):
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### 🏃‍♂️ Dati Prestazione & Ritmo")
                km_sett = st.number_input(f"Distanza Totale Settimana {settimana} (Km)", min_value=0.0, value=0.0, step=0.5, key=f"km_s_{settimana}")
                
                st.markdown("**Tempo Totale Settimana**")
                ts_h = st.number_input(f"Ore #{settimana}", 0, 10, 0, key=f"tsh_{settimana}")
                ts_m = st.number_input(f"Minuti #{settimana}", 0, 59, 0, key=f"tsm_{settimana}")
                
                ritmo_sett = st.selectbox(f"Ritmo Medio Settimana {settimana}", ritmi_disponibili, key=f"rit_s_{settimana}")
                
            with c2:
                st.markdown("#### ❤️ Dati Biometrici & Carico")
                bpm_max = st.number_input(f"BPM Massimo (Picco) - Sett. {settimana}", 0, 220, 0, key=f"bpm_max_{settimana}")
                minuto_max = st.text_input(f"A che minuto si è verificato il BPM Max? (es. 42° min) - Sett. {settimana}", key=f"min_max_{settimana}")
                
                bpm_min = st.number_input(f"BPM Minimo (Riposo/Recupero) - Sett. {settimana}", 0, 150, 0, key=f"bpm_min_{settimana}")
                cadenza = st.number_input(f"Cadenza Migliore (passi/min) - Sett. {settimana}", 0, 220, 0, key=f"cad_{settimana}")
                
                sforzo = st.slider(f"Sforzo Percepito Medio (1-10) - Sett. {settimana}", 1, 10, 5, key=f"sf_{settimana}")

            # Calcoli interni alla settimana
            sec_tempo_sett = (ts_h * 3600) + (ts_m * 60)
            
            sec_ritmo_sett = 0
            if ritmo_sett != "Seleziona ritmo...":
                mr, sr = map(int, ritmo_sett.split(":"))
                sec_ritmo_sett = mr * 60 + sr

            # Calcolo Carico (Volume x Sforzo)
            carico_settimana = ts_m * sforzo if ts_m > 0 else int(km_sett * 10 * sforzo)
            carico_tot_4s += carico_settimana

            if km_sett > 0:
                km_totali_4s += km_sett
            if sec_tempo_sett > 0:
                secondi_totali_4s += sec_tempo_sett
            if sec_ritmo_sett > 0:
                ritmi_validi_4s.append(sec_ritmo_sett)
            if bpm_max > 0:
                tutti_bpm_max.append((bpm_max, minuto_sett := minuto_max, settimana))
            if bpm_min > 0:
                tutti_bpm_min.append(bpm_min)
            if cadenza > 0:
                tutte_cadenze.append(cadenza)

            st.info(f"📊 **Carico Stimato Settimana {settimana}:** {carico_settimana} punti")

    # --- RIEPILOGO GLOBALE 4 SETTIMANE ---
    st.markdown("---")
    st.subheader("🏆 Riepilogo Generale Ciclo (4 Settimane)")

    col_g1, col_g2, col_g3 = st.columns(3)
    col_g1.metric("KM Totali 4 Settimane", f"{km_totali_4s:.2f} km")
    
    h_4s = secondi_totali_4s // 3600
    m_4s = (secondi_totali_4s % 3600) // 60
    str_t_4s = f"{h_4s}h {m_4s:02d}m" if h_4s > 0 else f"{m_4s}m"
    col_g2.metric("Tempo Totale Accumulato", str_t_4s)

    if ritmi_validi_4s:
        media_r_4s = sum(ritmi_validi_4s) / len(ritmi_validi_4s)
        str_r_4s = f"{int(media_r_4s // 60)}:{int(media_r_4s % 60):02d} /km"
    else:
        str_r_4s = "--:--"
    col_g3.metric("Ritmo Medio Globale", str_r_4s)

    # Sezione Biometrica Globale
    st.markdown("### ❤️ Quadro Biometrico Complessivo")
    b_col1, b_col2, b_col3 = st.columns(3)
    
    max_assoluto = max([x[0] for x in tutti_bpm_max]) if tutti_bpm_max else 0
    min_assoluto = min(tutti_bpm_min) if tutti_bpm_min else 0
    cadenza_media = int(sum(tutte_cadenze) / len(tutte_cadenze)) if tutte_cadenze else 0

    b_col1.metric("Picco Massimo BPM", f"{max_assoluto} bpm")
    b_col2.metric("Minimo BPM Registrato", f"{min_assoluto} bpm")
    b_col3.metric("Cadenza Media Ideale", f"{cadenza_media} spm")

    # Salvataggio del ciclo
    nome_ciclo = st.text_input("Nome da dare a questo ciclo di 4 settimane:", key="nome_ciclo_4s")
    if st.button("💾 Salva Ciclo 4 Settimane"):
        if nome_ciclo.strip():
            nuovo_ciclo = {
                "titolo": nome_ciclo,
                "km_totali": km_totali_4s,
                "tempo_totale": str_t_4s,
                "ritmo_medio": str_r_4s,
                "carico_totale": carico_tot_4s,
                "bpm_max": max_assoluto,
                "bpm_min": min_assoluto,
                "cadenza_media": cadenza_media
            }
            storico.append(nuovo_ciclo)
            salva_dati(storico)
            st.success("✅ Ciclo di 4 settimane salvato correttamente nell'archivio!")
        else:
            st.error("Inserisci un nome valido prima di salvare.")


# ==============================================================================
# SCHEDA 2: CALCOLO RAPIDO & RIPETUTE (Il tool flessibile)
# ==============================================================================
with tab_scelta2:
    st.subheader("⚡ Calcolo Rapido Frazioni & Ripetute")
    st.markdown("Usa questo spazio per calcolare al volo ritmi, distanze o tempi per singole ripetute.")

    num_blocchi = 10
    for i in range(1, num_blocchi + 1):
        with st.expander(f"Ripetuta / Blocco {i}", expanded=(i == 1)):
            c1, c2, c3 = st.columns(3)
            with c1:
                km_r = st.number_input(f"Distanza (Km) #{i}", min_value=0.0, value=0.0, step=0.1, key=f"r_km_{i}")
            with c2:
                tm_r = st.number_input(f"Minuti #{i}", 0, 300, 0, key=f"r_tm_{i}")
                ts_r = st.number_input(f"Secondi #{i}", 0, 59, 0, step=5, key=f"r_ts_{i}")
            with c3:
                rit_r = st.selectbox(f"Ritmo al Km #{i}", ritmi_disponibili, key=f"r_rit_{i}")

            sec_t = tm_r * 60 + ts_r
            if km_r > 0 and sec_t > 0 and rit_r == "Seleziona ritmo...":
                sec_calc = sec_t / km_r
                st.success(f"⚡ Ritmo calcolato: {int(sec_calc//60)}:{int(sec_calc%60):02d} /km")
            elif km_r > 0 and rit_r != "Seleziona ritmo..." and sec_t == 0:
                mr, sr = map(int, rit_r.split(":"))
                sec_tot = int((mr * 60 + sr) * km_r)
                st.success(f"⏱️ Tempo calcolato: {sec_tot//60}m {sec_tot%60:02d}s")


# ==============================================================================
# SCHEDA 3: STORICO SALVATO
# ==============================================================================
with tab_scelta3:
    st.subheader("📂 Archivio Cicli Salvati")
    if not storico:
        st.info("Nessun ciclo o sessione salvata al momento.")
    else:
        for idx, item in enumerate(storico):
            with st.expander(f"📌 {item.get('titolo', 'Sessione')} (ID: {idx+1})"):
                st.write(f"**KM Totali:** {item.get('km_totali', 0):.2f} km")
                st.write(f"**Tempo Totale:** {item.get('tempo_totale', 'N/D')}")
                st.write(f"**Ritmo Medio:** {item.get('ritmo_medio', 'N/D')}")
                if 'bpm_max' in item:
                    st.write(f"**BPM Max:** {item['bpm_max']} bpm | **BPM Min:** {item['bpm_min']} bpm | **Cadenza Media:** {item['cadenza_media']} spm")
                
                if st.button(f"🗑️ Elimina '{item.get('titolo', 'Elemento')}'", key=f"del_{idx}"):
                    storico.pop(idx)
                    salva_dati(storico)
                    st.rerun()
