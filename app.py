import streamlit as st
import os
from pipeline_run import analyser_reunion
from rag.memory import poser_question

st.set_page_config(page_title="Assistant de Reunion IA", page_icon="🎙️")

st.title("🎙️ Assistant Intelligent de Reunion")
st.write("Uploadez une reunion, l'IA extrait decisions, taches et compte-rendu.")

# Memoire de session (pour que les resultats ne disparaissent pas)
if "resume" not in st.session_state:
    st.session_state.resume = None
if "reponse" not in st.session_state:
    st.session_state.reponse = None

# ===== PARTIE 1 : ANALYSE =====
st.header("1. Analyser une reunion")
fichier = st.file_uploader("Choisissez votre reunion", type=["mp4", "m4a", "mp3", "wav"])

if fichier is not None:
    os.makedirs("uploads_temp", exist_ok=True)
    chemin = os.path.join("uploads_temp", fichier.name)
    with open(chemin, "wb") as f:
        f.write(fichier.getbuffer())
    st.success(f"Fichier recu : {fichier.name}")

    if st.button("🚀 Analyser la reunion"):
        with st.spinner("Les agents travaillent... (1-2 min)"):
            st.session_state.resume = analyser_reunion(chemin)

# Afficher le resume s'il existe (reste affiche meme apres un autre clic)
if st.session_state.resume:
    st.subheader("📋 Resume Executif")
    st.markdown(st.session_state.resume)
    st.info("✅ Reunion ajoutee a la memoire. Posez vos questions ci-dessous.")

# ===== PARTIE 2 : QUESTIONS (RAG) =====
st.header("2. Poser une question sur vos reunions")

st.write("Questions rapides :")
col1, col2, col3, col4 = st.columns(4)
question_cliquee = None
if col1.button("Decisions ?"):
    question_cliquee = "Quelles sont les decisions prises ?"
if col2.button("Taches ?"):
    question_cliquee = "Quelles sont les taches et qui en est responsable ?"
if col3.button("Echeances ?"):
    question_cliquee = "Quelles sont les echeances ?"
if col4.button("Blocages ?"):
    question_cliquee = "Y a-t-il des points de blocage ?"

question_tapee = st.text_input("Ou tapez votre propre question :")

question = question_cliquee or (question_tapee if st.button("🔍 Chercher") else None)

if question:
    with st.spinner("Recherche dans la memoire..."):
        st.session_state.reponse = poser_question(question)

if st.session_state.reponse:
    st.subheader("💡 Reponse")
    st.markdown(st.session_state.reponse)