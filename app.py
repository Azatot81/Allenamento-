import streamlit as st

st.set_page_config(page_title="Tool Calcolo Podismo", page_icon="🏃‍♂️", layout="centered")

st.title("🏃‍♂️ Mini-Tool Calcolo Allenamento")
st.markdown("Seleziona quale variabile vuoi calcolare inserendo i dati noti:")

# Creiamo dei tab per separare le 3 funzioni del mini-tool
tab1, tab2, tab3 = st.tabs(["Calcola Tempo", "Calcola Ritmo", "Calcola Distanza"])

# --- TAB 1: Calcola il Tempo Totale (Distanza + Ritmo) ---
with tab1:
    st.subheader("⏱️ Calcola il Tempo Totale")
    col1, col2 = st.columns(2)
    with col1:
        dist_km = st.number_input("Distanza (km)", min_value=0.1, value=10.0, step=0.1, key="t_km")
    with col2:
        st.markdown("Ritmo al km")
        c_min, c_sec = st.columns(2)
        with c_min:
            ritmo_min = st.number_input("Min", min_value=0, max_value=15, value=5, key="t_min")
        with c_sec:
            ritmo_sec = st.number_input("Sec", min_value=0, max_value=59, value=0, key="t_sec")
            
    if st.button("Calcola Tempo", key="btn_t"):
        tot_sec_per_km = (ritmo_min * 60) + ritmo_sec
        tot_sec = tot_sec_per_km * dist_km
        ore = int(tot_sec // 3600)
        minuti = int((tot_sec % 3600) // 60)
        secondi = int(tot_sec % 60)
        
        if ore > 0:
            risultato = f"{ore}h {minuti:02d}m {secondi:02d}s"
        else:
            risultato = f"{minuti}m {secondi:02d}s"
            
        st.success(f"### Tempo stimato: {risultato}")

# --- TAB 2: Calcola il Ritmo (Tempo Totale + Distanza) ---
with tab2:
    st.subheader("⚡ Calcola il Ritmo al Km")
    dist_km_2 = st.number_input("Distanza (km)", min_value=0.1, value=10.0, step=0.1, key="r_km")
    
    st.markdown("Tempo Totale Impiegato")
    c_h, c_m, c_s = st.columns(3)
    with c_h:
        t_ore = st.number_input("Ore", min_value=0, max_value=24, value=0, key="r_h")
    with c_m:
        t_min = st.number_input("Minuti", min_value=0, max_value=59, value=45, key="r_m")
    with c_s:
        t_sec = st.number_input("Secondi", min_value=0, max_value=59, value=0, key="r_s")
        
    if st.button("Calcola Ritmo", key="btn_r"):
        tot_sec = (t_ore * 3600) + (t_min * 60) + t_sec
        if dist_km_2 > 0:
            sec_al_km = tot_sec / dist_km_2
            r_min = int(sec_al_km // 60)
            r_sec = int(sec_al_km % 60)
            st.success(f"### Ritmo calcolato: {r_min}:{r_sec:02d} /km")
        else:
            st.error("La distanza deve essere maggiore di zero.")

# --- TAB 3: Calcola la Distanza (Tempo Totale + Ritmo) ---
with tab3:
    st.subheader("📏 Calcola la Distanza")
    st.markdown("Tempo Totale")
    c_h3, c_m3, c_s3 = st.columns(3)
    with c_h3:
        t_ore3 = st.number_input("Ore", min_value=0, max_value=24, value=0, key="d_h")
    with c_m3:
        t_min3 = st.number_input("Minuti", min_value=0, max_value=59, value=50, key="d_m")
    with c_s3:
        t_sec3 = st.number_input("Secondi", min_value=0, max_value=59, value=0, key="d_s")
        
    st.markdown("Ritmo al km tenuto")
    c_min3, c_sec3 = st.columns(2)
    with c_min3:
        ritmo_min3 = st.number_input("Min", min_value=0, max_value=15, value=5, key="d_rmin")
    with c_sec3:
        ritmo_sec3 = st.number_input("Sec", min_value=0, max_value=59, value=0, key="d_rsec")
        
    if st.button("Calcola Distanza", key="btn_d"):
        tot_sec_tempo = (t_ore3 * 3600) + (t_min3 * 60) + t_sec3
        sec_al_km3 = (ritmo_min3 * 60) + ritmo_sec3
        if sec_al_km3 > 0:
            km_calcolati = tot_sec_tempo / sec_al_km3
            st.success(f"### Distanza percorsa: {km_calcolati:.2f} km")
        else:
            st.error("Il ritmo non può essere zero.")
