import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Modele d'embeddings MULTILINGUE (arabe + francais + anglais)
embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-small"
)

# Dossier ou ChromaDB stocke la memoire (persiste sur le disque)
DB_DIR = "chroma_db"


def memoriser_reunion(texte, nom_reunion="reunion"):
    """Memorise une reunion. Si elle existe deja, remplace l'ancienne version (pas de doublon)."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    morceaux = splitter.split_text(texte)
    db = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings,
    )

    # Supprimer l'ancienne version de cette reunion (si elle existe deja)
    try:
        db.delete(where={"reunion": nom_reunion})
    except Exception as e:
        print(f"Pas d'ancienne version a supprimer : {e}")

    # Memoriser la nouvelle version
    db.add_texts(
        texts=morceaux,
        metadatas=[{"reunion": nom_reunion} for _ in morceaux],
    )
    return f"{len(morceaux)} morceaux memorises pour '{nom_reunion}'"


def poser_question(question):
    """Cherche dans la memoire et repond a la question avec le LLM."""
    db = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings,
    )
    # Trouver les 5 morceaux les plus pertinents (plus de contexte)
    resultats = db.similarity_search(question, k=5)
    contexte = "\n\n".join([doc.page_content for doc in resultats])

    # Demander au LLM de repondre a partir du contexte
    prompt = f"""Reponds a la question en te basant sur le contexte ci-dessous (transcription et analyse de reunions).
Le contexte peut contenir des dates ecrites de differentes facons (ex: "avant mercredi", "le 9 juillet", "echeances").
Cherche attentivement les informations pertinentes, meme si les mots exacts de la question n'apparaissent pas.
Si vraiment aucune information pertinente n'existe, dis "Information non trouvee dans les reunions".

Contexte :
{contexte}

Question : {question}

Reponse :"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content