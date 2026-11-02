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
    padding-bottom: 2rem;
    max-width: 95% !important;
}
div.stExpander, div.stTabs [data-baseweb="tab-panel"], section[data-testid="stSidebar"], div[data-testid="stVerticalBlock"] > div {
    background-color: rgba(255, 255, 255, 0.97) !important;
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

if "autenticato" not in st.session_state:
    st.session_state.autenticato = False

if not st.session_state.autenticato:
    st.subheader("🔒 Accesso Riservato")
    password_inserita = st.text_input("Inserisci la password per sbloccare l'app:", type="password", key="pass_input_login")
    if st.button("Accedi", key="btn_login_submit"):
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
    "📅 Gestione 4 Settimane", 
    "📊 Tabella & PDF",
    "📂 Archivio & Backup"
])

ritmi_disponibili = ["Seleziona ritmo..."]
for m in range(2, 7):
    for s in range(0, 60, 5):
        if (m == 2 and s >= 10) or (m > 2 and m < 6) or (m == 6 and s <= 15):
            ritmi_disponibili.append(f"{m}:{s:02d}")

def mostra_banner_sforzo(valore):
    colori_sforzo = {
        1: "Molto Leggero (Rigenerante)",
        2: "Leggero (Corsa lenta)",
        3: "Moderato (Fondo lungo)",
        4: "Medio-Basso (Progressivo)",
        5: "Medio (Ritmo medio)",
        6: "Impegnativo (Soglia)",
        7: "Forte (Corto veloce)",
        8: "Molto Forte (Ripetute brevi)",
        9: "Estenuante (Massima potenza)",
        10: "Massimale (Gara)"
    }
    desc = colori_sforzo.get(valore, "Normale")
    testo_banner = "🟡 Sforzo " + str(valore) + ": " + desc
    st.markdown('<div style="background-color: #fff3cd; color: #000000; padding: 8px; border-radius: 6px; text-align: center; font-weight: bold; margin-bottom: 10px; font-size: 14px; border: 1px solid #ffeeba;">' + testo_banner + '</div>', unsafe_allow_html=True)

with tab_scelta1:
    st.subheader("📋 Ciclo Mensile: 4 Settimane x 7 Giorni")
    
    titolo_predefinito = ""
    if st.session_state.edit_data:
        titolo_predefinito = st.session_state.edit_data.get("titolo", "")
        st.info(f"✏️ Stai modificando il piano: **{titolo_predefinito}**")

    settimana_scelta = st.selectbox("Seleziona la Settimana:", ["Settimana 1", "Settimana 2", "Settimana 3", "Settimana 4"], key="sel_settimana_principale")
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
            st.text_input(f"Descrizione Allenamento G{giorno}", key=desc_k)
            
            # Sezione PREVISTO
            st.markdown(f"#### 📋 Allenamento Previsto (Giorno {giorno})")
            km_prev = st.number_input(f"Km Previsti G{giorno}", min_value=0.0, value=0.0, step=0.1, key=k_p)
            min_prev = st.number_input(f"Minuti Previsti G{giorno}", min_value=0, max_value=300, value=0, key=m_p)
            rit_prev = st.selectbox(f"Ritmo Previsto G{giorno}", ritmi_disponibili, key=r_p_key)
            
            r_prev_auto = "--:--"
            if km_prev > 0 and min_prev > 0:
                sec_p_auto = (min_prev * 60) / km_prev
                r_prev_auto = f"{int(sec_p_auto // 60)}:{int(sec_p_auto % 60):02d}"
            
            st.markdown("⚡ **Ritmo Previsto Calcolato:** `" + r_prev_auto + " /km`")
            st.text_input(f"Ritmo previsto manuale G{giorno}", key=rc_p_key)
            st.markdown(f"**Sforzo Previsto G{giorno} (1-10)**")
            sf_prev = st.selectbox(f"Sforzo P G{giorno}", list(range(1, 11)), index=4, key=s_p)
            mostra_banner_sforzo(sf_prev)
            
            st.markdown("---")
            # Sezione EFFETTIVO
            st.markdown(f"#### ✅ Allenamento Effettivo (Giorno {giorno})")
            km_eff = st.number_input(f"Km Effettivi G{giorno}", min_value=0.0, value=0.0, step=0.1, key=k_e)
            min_eff = st.number_input(f"Minuti Effettivi G{giorno}", min_value=0, max_value=300, value=0, key=m_e)
            rit_eff = st.selectbox(f"Ritmo Effettivo G{giorno}", ritmi_disponibili, key=r_key)
            
            ritmo_calcolato_auto = "--:--"
            if km_eff > 0 and min_eff > 0:
                sec_tot_calc = (min_eff * 60) / km_eff
                m_calc = int(sec_tot_calc // 60)
                s_calc = int(sec_tot_calc % 60)
                ritmo_calcolato_auto = f"{m_calc}:{s_calc:02d}"

            st.markdown("⚡ **Ritmo Effettivo Calcolato:** `" + ritmo_calcolato_auto + " /km`")
            ritmo_inserito_utente = st.text_input(f"Ritmo effettivo manuale G{giorno}", key=rc_key)
            st.markdown(f"**Sforzo Effettivo G{giorno} (1-10)**")
            sf_eff = st.selectbox(f"Sforzo E G{giorno}", list(range(1, 11)), index=4, key=s_e)
            mostra_banner_sforzo(sf_eff)
            
            st.markdown("---")
            # Sezione BIOMETRIA
            st.markdown(f"#### ❤️ Dati Biometrici (Giorno {giorno})")
            b_max = st.number_input(f"BPM Max G{giorno}", 0, 220, 0, key=bmax_k)
            b_min = st.number_input(f"BPM Min G{giorno}", 0, 150, 0, key=bmin_k)
            cad = st.number_input(f"Cadenza G{giorno} (spm)", 0, 220, 0, key=cad_k)

            c_prev = min_prev * sf_prev if min_prev > 0 else int(km_prev * 10 * sf_prev)
            c_eff = min_eff * sf_eff if min_eff > 0 else int(km_eff * 10 * sf_eff)

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

            st.info("🔹 Carico Previsto: **" + str(c_prev) + " pt** | 🔸 Carico Effettivo: **" + str(c_eff) + " pt** | ⏱️ Ritmo Usato: **" + str(ritmo_finale_scelto) + " /km**")

    st.markdown("---")
    st.subheader("📊 Riepilogo - " + settimana_scelta)
    
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

    nome_salv = st.text_input("Nome piano di allenamento:", value=titolo_predefinito, key="nome_piano_28g_input")
    if st.button("💾 Salva Settimana / Aggiorna", key="btn_salva_settimana"):
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
            st.success("✅ Salvato correttamente!")
            st.session_state.edit_data = None
        else:
            st.error("Inserisci un nome valido.")

with tab_scelta2:
    st.subheader("📊 Schema Tabulare Completo (Stile Excel)")
    st.markdown("Prospetto riassuntivo dei 7 giorni della settimana selezionata, pronto per la stampa o l'esportazione PDF dal browser.")

    sett_tabella = st.selectbox("Visualizza Tabella per:", ["Settimana 1", "Settimana 2", "Settimana 3", "Settimana 4"], key="tab_s_sel_report")
    n_s_tab = int(sett_tabella.split(" ")[1])

    dati_tabella = []
    tot_km_p = 0.0
    tot_km_e = 0.0
    tot_min_p = 0
    tot_min_e = 0
    tot_carico_p = 0
    tot_carico_e = 0

    for g in range(1, 8):
        s_n = str(n_s_tab)
        g_n = str(g)
        
        desc = st.session_state.get(f"desc_s{s_n}_g{g_n}", f"Allenamento {g}")
        k_prev = st.session_state.get(f"p_km_s{s_n}_g{g_n}", 0.0)
        k_eff = st.session_state.get(f"e_km_s{s_n}_g{g_n}", 0.0)
        m_prev = st.session_state.get(f"p_min_s{s_n}_g{g_n}", 0)
        m_eff = st.session_state.get(f"e_min_s{s_n}_g{g_n}", 0)
        sf_p = st.session_state.get(f"p_sf_s{s_n}_g{g_n}", 5)
        sf_e = st.session_state.get(f"e_sf_s{s_n}_g{g_n}", 5)
        
        c_p = m_prev * sf_p if m_prev > 0 else int(k_prev * 10 * sf_p)
        c_e = m_eff * sf_e if m_eff > 0 else int(k_eff * 10 * sf_e)
        
        bmax = st.session_state.get(f"bmax_s{s_n}_g{g_n}", 0)
        cad = st.session_state.get(f"cad_s{s_n}_g{g_n}", 0)

        tot_km_p += k_prev
        tot_km_e += k_eff
        tot_min_p += m_prev
        tot_min_e += m_eff
        tot_carico_p += c_p
        tot_carico_e += c_e

        dati_tabella.append({
            "Giorno": f"Giorno {g}",
            "Descrizione": desc if desc else "-",
            "Km Prev.": f"{k_prev:.1f}",
            "Km Eff.": f"{k_eff:.1f}",
            "Min Prev.": m_prev,
            "Min Eff.": m_eff,
            "Sforzo P.": sf_p,
            "Sforzo E.": sf_e,
            "Carico Prev.": c_p,
            "Carico Eff.": c_e,
            "BPM Max": bmax if bmax > 0 else "-",
            "Cadenza": cad if cad > 0 else "-"
        })

    df_report = pd.DataFrame(dati_tabella)
    st.dataframe(df_report, use_container_width=True)

    st.markdown("### 📌 Totali " + sett_tabella)
    st.markdown("- **KM Previsti / Effettivi:** `" + f"{tot_km_p:.1f}" + " km` / `" + f"{tot_km_e:.1f}" + " km`")
    st.markdown("- **Minuti Previsti / Effettivi:** `" + str(tot_min_p) + " min` / `" + str(tot_min_e) + " min`")
    st.markdown("- **Carico Previsto / Effettivo:** `" + str(tot_carico_p) + " pt` / `" + str(tot_carico_e) + " pt`")

with tab_scelta3:
    st.subheader("📂 Archivio, Modifica & Backup Locale")
    
    json_string = json.dumps(storico, indent=4)
    st.download_button(
        label="📥 Scarica Backup Archivio sul Tablet/Smartphone (.json)",
        data=json_string,
        file_name="backup_allenamenti.json",
        mime="application/json",
        key="btn_download_backup"
    )
    
    st.markdown("---")
    uploaded_file = st.file_uploader("📤 Ripristina Backup da File JSON salvato sul Tablet:", type=["json"], key="uploader_backup_json")
    if uploaded_file is not None:
        try:
            dati_caricati = json.load(uploaded_file)
            if st.button("🔄 Conferma e Ripristina Backup", key="btn_conferma_ripristino"):
                salva_dati(dati_caricati)
                st.success("✅ Backup ripristinato con successo!")
                st.rerun()
        except Exception as e:
            st.error("Errore nella lettura del file JSON.")

    st.markdown("---")
    st.subheader("📋 Elenco Piani Salvati (Archivio)")
    if not storico:
        st.info("Nessun elemento salvato nell'archivio.")
    else:
        for idx, item in enumerate(storico):
            with st.expander("📌 " + str(item['titolo']) + " (" + str(item['settimana']) + ")"):
                st.write("**KM:** " + f"{item['km_settimana']:.2f}" + " | **Carico Effettivo:** " + str(item['carico_effettivo']) + " pt | **Ritmo Medio:** " + str(item['ritmo_medio']))
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("✏️ Modifica", key="edit_item_" + str(idx)):
                        st.session_state.edit_data = item
                        st.success("Caricato '" + str(item['titolo']) + "'. Torna alla scheda 'Gestione 4 Settimane'.")
                with col_btn2:
                    if st.button("🗑️ Elimina", key="del_item_" + str(idx)):
                        storico.pop(idx)
                        salva_dati(storico)
                        st.rerun()
