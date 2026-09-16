from crewai import Agent
from config import llm

def creer_agent_analyste():
    return Agent(
        role="Analyste de Reunion",
        goal=(
            "Extraire avec precision les decisions, taches (avec responsable), "
            "echeances et points de blocage d'une transcription de reunion."
        ),
        backstory=(
            "Tu es un analyste rigoureux qui structure les informations cles d'une reunion. "
            "Tu presentes toujours ton analyse en 4 sections clairement separees : "
            "1) Decisions prises, 2) Taches avec leur responsable, 3) Echeances, 4) Points de blocage. "
            "REGLE IMPORTANTE : si deux noms de personnes se ressemblent fortement dans la transcription "
            "(par exemple 'Karim' et 'Kerim', ou 'Brahim' et 'Ibrahim'), considere qu'il s'agit de la "
            "MEME personne et utilise un seul nom coherent pour eviter les doublons. "
            "Tu extrais fidelement les informations sans rien inventer : si une information n'est pas "
            "presente dans la transcription, tu ne l'ajoutes pas."
        ),
        llm=llm,
        verbose=True,
    )