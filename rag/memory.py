import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
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
    """Cherche dans la memoire et repond UNIQUEMENT a partir des reunions."""
    db = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings,
    )
    # Trouver les 5 morceaux les plus pertinents
    resultats = db.similarity_search(question, k=5)
    contexte = "\n\n".join([doc.page_content for doc in resultats])

    # Prompt STRICT : repond UNIQUEMENT depuis le contexte (anti-hallucination)
    prompt = f"""Tu es un assistant qui repond aux questions UNIQUEMENT a partir du contexte de reunions ci-dessous.

REGLES STRICTES :
- Utilise SEULEMENT les informations presentes dans le contexte ci-dessous.
- N'utilise JAMAIS tes connaissances generales (geographie, actualite, culture, etc.).
- Le contexte peut contenir des dates ecrites differemment (ex: "avant mercredi", "le 9 juillet").
- Si la reponse n'est PAS dans le contexte, reponds EXACTEMENT et UNIQUEMENT :
  "Cette information n'est pas disponible dans les reunions analysees."

Contexte des reunions :
{contexte}

Question : {question}

Reponse (basee uniquement sur le contexte) :"""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content