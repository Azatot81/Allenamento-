import streamlit as st
import json
import os

st.set_page_config(page_title="Tool Allenamento - 28 Giorni", layout="wide")

# --- CSS PERSONALIZZATO PER CONTRASTO PERFETTO SU SFONDO ROSA ---
sfondo_css = """
<style>
.stApp {
background-image: url("https://www.liceodonmilani.it/wp-content/uploads/2021/06/Schermata-2018-01-22-alle-12.49.06-980x490-1.png");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 95% !important;
}
div.stExpander, div.stTabs [data-baseweb="tab-panel"], section[data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.92) !important;
    border-radius: 10px;
    padding: 15px;
    color: #000000 !important;
}
h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: #111111 !important;
}
input, select, textarea, div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}
</style>
"""
st.markdown(sfondo_css, unsafe_allow_html=True)

# --- 1. PROTEZIONE PASSWORD ---
st.sidebar.header("Accesso Riservato")
password_inserita = st.sidebar.text_input("Inserisci la password:", type="password")
if password_inserita != "allenamento2026":
    st.warning("⚠️ Inserisci la password corretta nella barra laterale.")
    st.stop()
st.sidebar.success("Accesso Autorizzato!")

st.title("🏃‍♂️ Dashboard Allenamento (28 Giorni)")

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

tab_scelta1, tab_scelta2 = st.tabs([
    "📅 Gestione 4 Settimane (28 Giorni)", 
    "📂 Archivio Salvato"
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
        r_key = "rit_s" + s_n + "_g" + g_n
        rc_key = "rit_calc_s" + s_n + "_g" + g_n
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
                st.markdown("**Sforzo Previsto (1-10)**")
                sf_prev = st.selectbox("", list(range(1, 11)), index=4, key=s_p)
                mostra_banner_sforzo(sf_prev)
                
            with c2:
                st.markdown("#### ✅ Effettivo")
                km_eff = st.number_input("Km Effettivi", min_value=0.0, value=0.0, step=0.1, key=k_e)
                min_eff = st.number_input("Minuti Effettivi", min_value=0, max_value=300, value=0, key=m_e)
                rit_eff = st.selectbox("Ritmo Effettivo", ritmi_disponibili, key=r_key)
                
                # Calcolo automatico o inserimento manuale del ritmo
                ritmo_calcolato_auto = "--:--"
                if km_eff > 0 and min_eff > 0:
                    sec_tot_calc = (min_eff * 60) / km_eff
                    m_calc = int(sec_tot_calc // 60)
                    s_calc = int(sec_tot_calc % 60)
                    ritmo_calcolato_auto = f"{m_calc}:{s_calc:02d}"

                st.markdown(f"⚡ **Ritmo Calcolato Automatico:** `{ritmo_calcolato_auto} /km`")
                ritmo_inserito_utente = st.text_input("O inserisci/correggi il ritmo manualmente (es. 4:30):", key=rc_key)

                st.markdown("**Sforzo Effettivo (1-10)**")
                sf_eff = st.selectbox("", list(range(1, 11)), index=4, key=s_e)
                mostra_banner_sforzo(sf_eff)
                
            with c3:
                st.markdown("#### ❤️ Biometria")
                b_max = st.number_input("BPM Max", 0, 220, 0, key=bmax_k)
                b_min = st.number_input("BPM Min", 0, 150, 0, key=bmin_k)
                cad = st.number_input("Cadenza (spm)", 0, 220, 0, key=cad_k)

            c_prev = min_prev * sf_prev if min_prev > 0 else int(km_prev * 10 * sf_prev)
            c_eff = min_eff * sf_eff if min_eff > 0 else int(km_eff * 10 * sf_eff)

            # Scegliamo quale ritmo considerare per le medie (priorità al manuale inserito, poi automatico, poi tendina)
            ritmo_finale_scelto = ritmo_inserito_utente.strip() if ritmo_inserito_utente.strip() else (ritmo_calcolato_auto if ritmo_calcolato_auto != "--:--" else rit_eff)
            
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
            if b_min > 0 and b_min < bpm_min_sett:
                bpm_min_sett = b_min

            st.info(f"🔹 Carico Previsto: **{c_prev} pt** | 🔸 Carico Effettivo: **{c_eff} pt** | ⏱️ Ritmo Usato: **{ritmo_finale_scelto} /km**")

    st.markdown("---")
    st.subheader(f"📊 Riepilogo - Settimana {num_sett}")
    
    cs1, cs2, cs3, cs4 = st.columns(4)
    cs1.metric("KM Totali", f"{km_sett_tot:.2f} km")
    cs2.metric("Carico Previsto", f"{carico_prev_tot} pt")
    cs3.metric("Carico Effettivo", f"{carico_eff_tot} pt")
    
    if ritmi_sett:
        m_rs = sum(ritmi_sett) / len(ritmi_sett)
        str_r = f"{int(m_rs // 60)}:{int(m_rs % 60):02d} /km"
    else:
        str_r = "--:--"
    cs4.metric("Ritmo Medio", str_r)

    nome_salv = st.text_input("Nome piano:", key="nome_piano_28g")
    if st.button("💾 Salva Settimana"):
        if nome_salv.strip():
            storico.append({
                "titolo": nome_salv,
                "settimana": settimana_scelta,
                "km_settimana": km_sett_tot,
                "carico_previsto": carico_prev_tot,
                "carico_effettivo": carico_eff_tot,
                "ritmo_medio": str_r
            })
            salva_dati(storico)
            st.success("✅ Salvato con successo!")
        else:
            st.error("Inserisci un nome valido.")

with tab_scelta2:
    st.subheader("📂 Archivio")
    if not storico:
        st.info("Nessun elemento salvato.")
    else:
        for idx, item in enumerate(storico):
            with st.expander(f"📌 {item['titolo']} ({item['settimana']})"):
                st.write(f"**KM:** {item['km_settimana']:.2f} | **Carico Effettivo:** {item['carico_effettivo']} pt | **Ritmo:** {item['ritmo_medio']}")
                if st.button(f"🗑️ Elimina", key=f"del_{idx}"):
                    storico.pop(idx)
                    salva_dati(storico)
                    st.rerun()
