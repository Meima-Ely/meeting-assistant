from crewai import Crew, Process
from agents.transcription import agent_transcription
from agents.analyste import agent_analyste
from agents.synthese import agent_synthese
from crewai import Task

def analyser_reunion(chemin_fichier):
    """Lance les 3 agents sur le fichier donne et retourne le compte-rendu."""

    tache_transcription = Task(
        description=f"Transcris l'audio du fichier '{chemin_fichier}' en utilisant ton outil de transcription.",
        expected_output="Le texte complet de la transcription de la reunion.",
        agent=agent_transcription,
    )
    tache_analyse = Task(
        description=(
            "A partir de la transcription, extrais et liste clairement : "
            "1) les decisions prises, 2) les taches avec leur responsable, "
            "3) les echeances, 4) les points de blocage."
        ),
        expected_output="Une liste structuree des decisions, taches, echeances et blocages.",
        agent=agent_analyste,
        context=[tache_transcription],
    )
    tache_synthese = Task(
        description="Redige un compte-rendu professionnel de la reunion a partir de l'analyse.",
        expected_output="Un compte-rendu clair et bien organise de la reunion.",
        agent=agent_synthese,
        context=[tache_analyse],
    )

    crew = Crew(
        agents=[agent_transcription, agent_analyste, agent_synthese],
        tasks=[tache_transcription, tache_analyse, tache_synthese],
        process=Process.sequential,
        verbose=True,
    )
    resultat = crew.kickoff()
    return str(resultat)