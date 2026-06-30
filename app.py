import streamlit as st
import os
from pipeline_run import analyser_reunion

st.set_page_config(page_title="Assistant de Reunion IA", page_icon="🎙️")

st.title("🎙️ Assistant Intelligent de Reunion")
st.write("Uploadez une reunion, l'IA extrait decisions, taches et compte-rendu.")

# Upload de n'importe quel fichier
fichier = st.file_uploader("Choisissez votre reunion", type=["mp4", "m4a", "mp3", "wav"])

if fichier is not None:
    # Sauvegarder le fichier uploade
    chemin = os.path.join("uploads_temp", fichier.name)
    os.makedirs("uploads_temp", exist_ok=True)
    with open(chemin, "wb") as f:
        f.write(fichier.getbuffer())

    st.success(f"Fichier recu : {fichier.name}")

    if st.button("🚀 Analyser la reunion"):
        with st.spinner("Les agents travaillent... (transcription, analyse, synthese)"):
            resultat = analyser_reunion(chemin)
        st.subheader("📋 Compte-Rendu")
        st.markdown(resultat)