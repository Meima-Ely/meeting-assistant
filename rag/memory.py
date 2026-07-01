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
    """Decoupe une reunion en morceaux et la stocke dans la memoire RAG."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    morceaux = splitter.split_text(texte)

    db = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings,
    )
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
    # Trouver les 3 morceaux les plus pertinents
    resultats = db.similarity_search(question, k=3)
    contexte = "\n\n".join([doc.page_content for doc in resultats])

    # Demander au LLM de repondre a partir du contexte
    prompt = f"""Reponds a la question en te basant UNIQUEMENT sur le contexte ci-dessous.
Si la reponse n'est pas dans le contexte, dis "Information non trouvee dans les reunions".

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