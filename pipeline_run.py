from crewai import Crew, Process, Task
from agents.transcription import agent_transcription
from agents.analyste import agent_analyste
from agents.synthese import agent_synthese
from rag.memory import memoriser_reunion


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
        description=(
            "A partir de l'analyse, redige un RESUME EXECUTIF de 2 a 3 phrases maximum. "
            "Capture uniquement l'essentiel : le sujet de la reunion, les decisions majeures, "
            "et l'etat global du projet. "
            "Ne liste pas les details (deja fait par l'analyste). "
            "Sois percutant et factuel. Aucune phrase de remplissage."
        ),
        expected_output="Un resume executif de 2 a 3 phrases, percutant et factuel.",
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

    analyse = str(tache_analyse.output)

    # Memoriser la transcription ET l'analyse structuree dans le RAG
    try:
        transcription = str(tache_transcription.output)
        # On memorise les deux : le brut + l'analyse (decisions, taches, echeances, blocages)
        texte_complet = (
            f"TRANSCRIPTION DE LA REUNION :\n{transcription}\n\n"
            f"ANALYSE STRUCTUREE (decisions, taches, echeances, blocages) :\n{analyse}"
        )
        memoriser_reunion(texte_complet, nom_reunion=chemin_fichier)
    except Exception as e:
        print(f"Memorisation RAG echouee : {e}")

    return {"resume": str(resultat), "analyse": analyse}