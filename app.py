import streamlit as st
import os
from pipeline_run import analyser_reunion
from rag.memory import poser_question
from mcp.github_connector import creer_issues_depuis_analyse
from mcp.telegram_connector import notifier_taches_creees
from mcp.pdf_generator import generer_pdf
from agents.compteur import compter_elements

st.set_page_config(
    page_title="Assistant de Reunion IA",
    page_icon="🎙️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-header { display: flex; align-items: center; gap: 14px; padding: 8px 0 4px 0; }
    .header-icon { width: 52px; height: 52px; border-radius: 14px; background: #E6F1FB; display: flex; align-items: center; justify-content: center; font-size: 26px; }
    .stButton>button { border-radius: 8px; font-weight: 500; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="main-header">
        <div class="header-icon">🎙️</div>
        <div>
            <div style="font-weight:600; font-size:22px;">Assistant Intelligent de Réunion</div>
            <div style="color:#6B7280; font-size:14px;">Transcription multilingue · Analyse IA · Mémoire RAG · Actions MCP</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

# Memoire de session
for cle in ["resume", "analyse", "reponse", "issues", "compteurs", "derniere_question"]:
    if cle not in st.session_state:
        st.session_state[cle] = None

# ===== SECTION UPLOAD =====
st.subheader("📤 Analyser une réunion")
col_up, col_btn = st.columns([3, 1])
with col_up:
    fichier = st.file_uploader("Fichier audio/vidéo", type=["mp4", "m4a", "mp3", "wav"], label_visibility="collapsed")
with col_btn:
    lancer = st.button("🚀 Analyser", use_container_width=True, type="primary")

if fichier is not None and lancer:
    os.makedirs("uploads_temp", exist_ok=True)
    chemin = os.path.join("uploads_temp", fichier.name)
    with open(chemin, "wb") as f:
        f.write(fichier.getbuffer())
    with st.spinner("Les agents IA travaillent... (1-2 min)"):
        resultat = analyser_reunion(chemin)
        st.session_state.resume = resultat["resume"]
        st.session_state.analyse = resultat["analyse"]
        st.session_state.issues = None
        st.session_state.compteurs = compter_elements(resultat["analyse"])

# ===== METRIQUES (vrais chiffres du LLM) =====
if st.session_state.analyse and st.session_state.compteurs:
    st.write("")
    c = st.session_state.compteurs
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📋 Décisions", c["decisions"])
    m2.metric("✅ Tâches", c["taches"])
    m3.metric("📅 Échéances", c["echeances"])
    m4.metric("⚠️ Blocages", c["blocages"])

# ===== 2 COLONNES : RESUME + MCP =====
if st.session_state.resume:
    st.write("")
    col_gauche, col_droite = st.columns(2, gap="medium")

    with col_gauche:
        with st.container(border=True):
            st.markdown("##### 📄 Résumé exécutif")
            st.write(st.session_state.resume)
            st.caption("✅ Mémorisé dans le RAG")

            if st.session_state.analyse:
                chemin_pdf = generer_pdf(st.session_state.resume, st.session_state.analyse)
                with open(chemin_pdf, "rb") as f:
                    st.download_button(
                        "📄 Télécharger le PDF",
                        data=f,
                        file_name="compte_rendu_reunion.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )

    with col_droite:
        with st.container(border=True):
            st.markdown("##### 🔧 Tâches → GitHub (MCP)")
            if st.button("Créer les issues GitHub", use_container_width=True):
                with st.spinner("Création des issues..."):
                    st.session_state.issues = creer_issues_depuis_analyse(st.session_state.analyse)

            if st.session_state.issues:
                st.success(f"✅ {len(st.session_state.issues)} issues créées")
                for issue in st.session_state.issues:
                    st.markdown(f"• **{issue['tache']}** · _{issue['responsable']}_ → [Issue]({issue['url']})")
                if notifier_taches_creees(st.session_state.issues, os.environ.get("GITHUB_REPO")):
                    st.caption("📱 Notifié sur Telegram")
            else:
                st.caption("Cliquez pour transformer les tâches en issues suivies.")

# ===== SECTION RAG (CHAT) =====
if st.session_state.resume:
    st.write("")
    with st.container(border=True):
        st.markdown("##### 💬 Interroger vos réunions (RAG)")
        st.caption("Questions rapides :")
        c1, c2, c3, c4 = st.columns(4)
        question_cliquee = None
        if c1.button("Décisions ?", use_container_width=True):
            question_cliquee = "Quelles sont les decisions prises ?"
        if c2.button("Tâches ?", use_container_width=True):
            question_cliquee = "Quelles sont les taches et qui en est responsable ?"
        if c3.button("Échéances ?", use_container_width=True):
            question_cliquee = "Quelles sont les echeances ?"
        if c4.button("Blocages ?", use_container_width=True):
            question_cliquee = "Y a-t-il des points de blocage ?"

        question_tapee = st.chat_input("Posez votre question sur les réunions...")
        question = question_cliquee or question_tapee

        if question:
            with st.spinner("Recherche dans la mémoire..."):
                st.session_state.reponse = poser_question(question)
            st.session_state.derniere_question = question

        if st.session_state.reponse:
            with st.chat_message("user"):
                st.write(st.session_state.derniere_question or "Question")
            with st.chat_message("assistant"):
                st.write(st.session_state.reponse)

st.divider()
st.caption("Assistant Intelligent de Réunion · PFE · CrewAI + Groq + RAG + MCP")