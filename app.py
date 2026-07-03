import streamlit as st
import os
from datetime import datetime
from pipeline_run import analyser_reunion
from rag.memory import poser_question
from mcp.github_connector import creer_issues_depuis_analyse
from mcp.telegram_connector import notifier_taches_creees
from mcp.pdf_generator import generer_pdf
from agents.compteur import compter_elements
from style import CSS

st.set_page_config(
    page_title="Assistant Intelligent de Réunion",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Appliquer le design (CSS isole dans style.py)
st.markdown(CSS, unsafe_allow_html=True)

# ===== SESSION STATE =====
for cle in ["resume", "analyse", "reponse", "issues", "compteurs", "chat"]:
    if cle not in st.session_state:
        st.session_state[cle] = None
if st.session_state.chat is None:
    st.session_state.chat = []

# ===== HEADER =====
statut = "● Système actif" if st.session_state.resume else "● Prêt"
st.markdown(f"""
<div class="hdr">
  <div class="hdr-icon">🎙️</div>
  <div>
    <div class="hdr-title">Assistant Intelligent de Réunion</div>
    <div class="hdr-sub">Transcription multilingue · Analyse IA · Mémoire RAG · MCP</div>
  </div>
  <div class="hdr-badge">{statut}</div>
</div>
""", unsafe_allow_html=True)

# ===== UPLOAD =====
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; padding:10px 0 6px;">
  <div style="font-size:34px;">📤</div>
  <div style="font-size:16px; font-weight:600; color:#0f172a; margin:8px 0 3px;">Déposez votre fichier audio ici</div>
  <div style="font-size:13px; color:#64748b;">MP4, MP3, WAV, M4A — analyse par vos 3 agents IA</div>
</div>
""", unsafe_allow_html=True)

fichier = st.file_uploader("Fichier", type=["mp4", "m4a", "mp3", "wav"], label_visibility="collapsed")

if fichier is not None:
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown(f"<div style='font-size:13px; color:#0f172a; padding-top:8px;'>🎵 <b>{fichier.name}</b> · {fichier.size/1024/1024:.1f} MB</div>", unsafe_allow_html=True)
    with c2:
        lancer = st.button("✨ Analyser", use_container_width=True)

    if lancer:
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
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===== METRIQUES (vrais chiffres) =====
if st.session_state.compteurs:
    c = st.session_state.compteurs
    donnees = [
        ("💡", "#f5f3ff", "Décisions", c["decisions"], "Prises"),
        ("✅", "#eff6ff", "Tâches", c["taches"], "Assignées"),
        ("📅", "#fffbeb", "Échéances", c["echeances"], "Identifiées"),
        ("⚠️", "#fff1f2", "Blocages", c["blocages"], "Identifiés"),
    ]
    cols = st.columns(4)
    for col, (ic, bg, label, n, tag) in zip(cols, donnees):
        with col:
            st.markdown(f"""
            <div class="metric">
              <div class="metric-ic" style="background:{bg};">{ic}</div>
              <div class="metric-n">{n}</div>
              <div class="metric-l">{label}</div>
              <div class="metric-t">{tag}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ===== RESUME + GITHUB =====
if st.session_state.resume:
    col_g, col_d = st.columns(2, gap="medium")

    with col_g:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        date_str = datetime.now().strftime("%d/%m/%Y")
        st.markdown(f"""
        <p class="card-title">📋 Résumé exécutif</p>
        <p class="card-sub">🕐 Analysé le {date_str}</p>
        <div class="hr"></div>
        """, unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:13.5px; color:#0f172a; line-height:1.7;'>{st.session_state.resume}</div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="margin-top:14px;">
          <span class="tag">Multilingue</span>
          <span class="tag">RAG</span>
          <span class="tag">MCP</span>
          <span class="tag">Mémorisé</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        chemin_pdf = generer_pdf(st.session_state.resume, st.session_state.analyse)
        with open(chemin_pdf, "rb") as f:
            st.download_button("⬇️ Télécharger le compte-rendu PDF", data=f,
                               file_name="compte_rendu_reunion.pdf", mime="application/pdf",
                               use_container_width=True)

    with col_d:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        nb = len(st.session_state.issues) if st.session_state.issues else 0
        sous_titre = f"{nb} issues créées automatiquement" if st.session_state.issues else "Prêt à créer les tâches"
        tg = '<span class="badge-tg">🔔 Notifié sur Telegram</span>' if st.session_state.issues else ''
        st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:space-between;">
          <div>
            <p class="card-title">🐙 Tâches GitHub (MCP)</p>
            <p class="card-sub">{sous_titre}</p>
          </div>
          {tg}
        </div>
        <div class="hr"></div>
        """, unsafe_allow_html=True)

        if not st.session_state.issues:
            if st.button("🔧 Créer les issues sur GitHub", use_container_width=True):
                with st.spinner("Création des issues..."):
                    st.session_state.issues = creer_issues_depuis_analyse(st.session_state.analyse)
                    notifier_taches_creees(st.session_state.issues, os.environ.get("GITHUB_REPO"))
                st.rerun()
        else:
            for issue in st.session_state.issues:
                initiales = "".join([m[0].upper() for m in issue["responsable"].split()[:2]]) if issue["responsable"] != "Non specifie" else "?"
                st.markdown(f"""
                <div class="task">
                  <div class="dot"></div>
                  <div style="flex:1; min-width:0;">
                    <span class="task-id">Issue</span>
                    <span class="pill-open">Ouvert</span>
                    <div class="task-title">{issue['tache']}</div>
                    <div class="task-meta"><span class="avatar">{initiales}</span>{issue['responsable']}
                      &nbsp;·&nbsp;<a href="{issue['url']}" target="_blank" style="color:#2E6FED; text-decoration:none;">Voir ↗</a>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# ===== CHAT RAG =====
if st.session_state.resume:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px;">
      <div style="width:32px; height:32px; background:#eef3fd; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:16px;">💬</div>
      <div>
        <p class="card-title" style="font-size:15px;">Interroger vos réunions</p>
        <p class="card-sub">Recherche sémantique (RAG) sur tout l'historique</p>
      </div>
    </div>
    <div class="hr"></div>
    """, unsafe_allow_html=True)

    for msg in st.session_state.chat:
        if msg["role"] == "user":
            st.markdown(f'<div class="bubble-u">{msg["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bubble-a">{msg["text"]}</div>', unsafe_allow_html=True)

    st.markdown("<div style='font-size:12.5px; color:#64748b; margin-bottom:6px;'>Questions rapides :</div>", unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)
    question = None
    if q1.button("Décisions", use_container_width=True):
        question = "Quelles sont les decisions prises dans la reunion ?"
    if q2.button("Tâches", use_container_width=True):
        question = "Quelles sont les taches et qui en est responsable ?"
    if q3.button("Échéances", use_container_width=True):
        question = "Quelles sont les dates limites, deadlines et delais mentionnes dans la reunion ?"
    if q4.button("Blocages", use_container_width=True):
        question = "Y a-t-il des points de blocage ou problemes dans la reunion ?"

    saisie = st.chat_input("Posez une question sur vos réunions...")
    if saisie:
        question = saisie

    if question:
        st.session_state.chat.append({"role": "user", "text": question})
        with st.spinner("Recherche dans la mémoire..."):
            rep = poser_question(question)
        st.session_state.chat.append({"role": "assistant", "text": rep})
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><div style='text-align:center; font-size:12px; color:#94a3b8;'>Assistant Intelligent de Réunion · PFE · CrewAI + Groq + RAG + MCP</div>", unsafe_allow_html=True)