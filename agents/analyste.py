from crewai import Agent
from config import llm

agent_analyste = Agent(
    role="Analyste de Reunion",
    goal="Extraire les decisions, taches, echeances et points de blocage d'une transcription",
    backstory="Tu es un analyste rigoureux qui structure les informations cles d'une reunion.",
    llm=llm,
    verbose=True,
)