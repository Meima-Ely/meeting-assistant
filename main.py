from crewai import Crew, Process
from agents.transcription import agent_transcription
from agents.analyste import agent_analyste
from agents.synthese import agent_synthese
from tasks import tache_transcription, tache_analyse, tache_synthese

crew = Crew(
    agents=[agent_transcription, agent_analyste, agent_synthese],
    tasks=[tache_transcription, tache_analyse, tache_synthese],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    print("Lancement du systeme multi-agents...\n")
    resultat = crew.kickoff()
    print("\n" + "=" * 60)
    print("COMPTE-RENDU FINAL :")
    print("=" * 60)
    print(resultat)