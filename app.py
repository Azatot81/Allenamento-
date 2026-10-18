import streamlit as st
import json
import os

st.set_page_config(page_title="Tool Allenamento Corsi", layout="wide")

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

st.title("🏃‍♂️ Gestione Completa Allenamenti & Carichi")

# --- GESTIONE ARCHIVIO DATI (SALVATAGGIO) ---
FILE_DATI = "storico_allenamenti.json"

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
    "⚡ Calcolo Ripetute & Mini-Tool", 
    "📊 Grafico Allenamenti 7 Giorni", 
    "📂 Storico Salvato"
])

# ==============================================================================
# SCHEDA 1: CALCOLO RIPETUTE
# ==============================================================================
with tab_scelta1:
    st.subheader("Gestione Frazioni & Ripetute")
    st.markdown("Inserisci le frazioni o le ripetute: l'app calcolerà all'istante il dato mancante e i totali finali.")

    ritmi_disponibili = ["Seleziona ritmo..."]
    for m in range(2, 7):
        for s in range(0, 60, 5):
            if (m == 2 and s >= 10) or (m > 2 and m < 6) or (m == 6 and s <= 15):
                ritmi_disponibili.append(f"{m}:{s:02d}")

    num_blocchi = 10
    km_totali_gen = 0.0
    secondi_totali_gen = 0
    ritmi_validi_gen = []

    st.markdown("---")
    sessione_corrente = []
    
    for i in range(1, num_blocchi + 1):
        with st.expander(f"Ripetuta / Blocco {i}", expanded=(i == 1)):
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                km = st.number_input(f"Distanza (Km) #{i}", min_value=0.0, max_value=100.0, value=0.0, step=0.1, key=f"km_{i}")
            with c2:
                st.markdown("**Tempo Totale**")
                t_min = st.number_input(f"Min #{i}", min_value=0, max_value=300, value=0, key=f"tm_{i}")
                t_sec = st.number_input(f"Sec #{i}", min_value=0, max_value=59, value=0, step=5, key=f"ts_{i}")
            with c3:
                ritmo_scelto = st.selectbox(f"Ritmo al Km #{i}", ritmi_disponibili, key=f"rit_{i}")
            
            sec_tempo_inserito = t_min * 60 + t_sec
            sec_ritmo_scelto = 0
            if ritmo_scelto != "Seleziona ritmo...":
                mr, sr = map(int, ritmo_scelto.split(":"))
                sec_ritmo_scelto = mr * 60 + sr
                
            risultato_riga = ""
            if km > 0 and sec_tempo_inserito > 0 and ritmo_scelto == "Seleziona ritmo...":
                sec_r = sec_tempo_inserito / km
                rm = int(sec_r // 60)
                rs = int(sec_r % 60)
                risultato_riga = f"⚡ **Ritmo calcolato:** {rm}:{rs:02d} /km"
                sec_ritmo_scelto = sec_r
            elif km > 0 and sec_ritmo_scelto > 0 and sec_tempo_inserito == 0:
                sec_t = int(sec_ritmo_scelto * km)
                tm_calc = sec_t // 60
                ts_calc = sec_t % 60
                risultato_riga = f"⏱️ **Tempo calcolato:** {tm_calc}m {ts_calc:02d}s"
                sec_tempo_inserito = sec_t
            elif km == 0.0 and sec_tempo_inserito > 0 and sec_ritmo_scelto > 0:
                km_calc = round(sec_tempo_inserito / sec_ritmo_scelto, 2)
                risultato_riga = f"📏 **Distanza calcolata:** {km_calc} km"
                km = km_calc

            if risultato_riga:
                st.success(risultato_riga)

            if km > 0 or sec_tempo_inserito > 0:
                sessione_corrente.append({"blocco": i, "km": km, "tempo_sec": sec_tempo_inserito, "ritmo": ritmo_scelto})

            if km > 0:
                km_totali_gen += km
            if sec_tempo_inserito > 0:
                secondi_totali_gen += sec_tempo_inserito
            if sec_ritmo_scelto > 0:
                ritmi_validi_gen.append(sec_ritmo_scelto)

    st.markdown("---")
    st.subheader("📊 Riepilogo Totale")
    col_tot1, col_tot2, col_tot3 = st.columns(3)
    col_tot1.metric("Distanza Totale", f"{km_totali_gen:.2f} km")

    h_t = secondi_totali_gen // 3600
    m_t = (secondi_totali_gen % 3600) // 60
    s_t = secondi_totali_gen % 60
    str_t_gen = f"{h_t}h {m_t:02d}m {s_t:02d}s" if h_t > 0 else f"{m_t}m {s_t:02d}s"
    col_tot2.metric("Tempo Totale", str_t_gen)

    if ritmi_validi_gen:
        media_r = sum(ritmi_validi_gen) / len(ritmi_validi_gen)
        str_r_gen = f"{int(media_r // 60)}:{int(media_r % 60):02d} /km"
    else:
        str_r_gen = "--:--"
    col_tot3.metric("Ritmo Medio Generale", str_r_gen)

    # Pulsante per salvare la sessione
    nome_sessione = st.text_input("Nome da dare a questa sessione di allenamento (es. Test 10km):", key="nome_sess")
    if st.button("💾 Salva questa Sessione"):
        if nome_sessione.strip():
            nuovo_salvataggio = {
                "titolo": nome_sessione,
                "km_totali": km_totali_gen,
                "tempo_totale": str_t_gen,
                "ritmo_medio": str_r_gen,
                "dettagli": sessione_corrente
            }
            storico.append(nuovo_salvataggio)
            salva_dati(storico)
            st.success("✅ Sessione salvata con successo! La trovi nella scheda 'Storico Salvato'.")
        else:
            st.error("Inserisci un nome valido per la sessione prima di salvare.")


# ==============================================================================
# SCHEDA 2: GRAFICO SETTIMANALE
# ==============================================================================
with tab_scelta2:
    st.subheader("📈 Tabella Sette Giorni - Previsioni vs Effettivi & Carichi")
    
    carico_prev_tot = 0.0
    carico_eff_tot = 0.0
    km_prev_tot = 0.0
    km_eff_tot = 0.0

    for allenamento in range(1, 8):
        with st.expander(f"Allenamento #{allenamento}", expanded=(allenamento == 1)):
            c_prev, c_eff = st.columns(2)
            with c_prev:
                st.markdown("#### 📋 Previsto")
                p_min = st.number_input(f"Minuti Previsti #{allenamento}", min_value=0, max_value=300, value=0, key=f"p_min_{allenamento}")
                p_km = st.number_input(f"Km Previsti #{allenamento}", min_value=0.0, max_value=100.0, value=0.0, step=0.1, key=f"p_km_{allenamento}")
                p_sforzo = st.slider(f"Sforzo Previsto (1-10) #{allenamento}", 1, 10, 5, key=f"p_sf_{allenamento}")
            with c_eff:
                st.markdown("#### ✅ Effettivo")
                e_min = st.number_input(f"Minuti Effettivi #{allenamento}", min_value=0, max_value=300, value=0, key=f"e_min_{allenamento}")
                e_km = st.number_input(f"Km Effettivi #{allenamento}", min_value=0.0, max_value=100.0, value=0.0, step=0.1, key=f"e_km_{allenamento}")
                e_sforzo = st.slider(f"Sforzo Effettivo (1-10) #{allenamento}", 1, 10, 5, key=f"e_sf_{allenamento}")

            carico_previsto_singolo = p_min * p_sforzo
            carico_effettivo_singolo = e_min * e_sforzo
            carico_prev_tot += carico_previsto_singolo
            carico_eff_tot += carico_effettivo_singolo
            km_prev_tot += p_km
            km_eff_tot += e_km

            st.info(f"🔹 **Carico Previsto:** {carico_previsto_singolo} | 🔸 **Carico Effettivo:** {carico_effettivo_singolo}")

    st.markdown("---")
    col_es1, col_es2 = st.columns(2)
    with col_es1:
        st.metric("KM Totali Previsti", f"{km_prev_tot:.2f} km")
        st.metric("Carico Totale Previsto", f"{carico_prev_tot:.0f}")
    with col_es2:
        st.metric("KM Totali Effettivi", f"{km_eff_tot:.2f} km")
        st.metric("Carico Totale Effettivo", f"{carico_eff_tot:.0f}")


# ==============================================================================
# SCHEDA 3: STORICO SALVATO (Per ripescare i dati)
# ==============================================================================
with tab_scelta3:
    st.subheader("📂 Archivio Sessioni Salvate")
    st.markdown("Qui puoi ripescare tutte le sessioni salvate in precedenza.")

    if not storico:
        st.info("Nessuna sessione salvata al momento.")
    else:
        for idx, item in enumerate(storico):
            with st.expander(f"📌 {item['titolo']} (ID: {idx+1})"):
                st.write(f"**Distanza Totale:** {item['km_totali']:.2f} km")
                st.write(f"**Tempo Totale:** {item['tempo_totale']}")
                st.write(f"**Ritmo Medio:** {item['ritmo_medio']}")
                
                if st.button(f"🗑️ Elimina sessione '{item['titolo']}'", key=f"del_{idx}"):
                    storico.pop(idx)
                    salva_dati(storico)
                    st.rerun()
