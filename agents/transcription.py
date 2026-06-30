from crewai import Agent
from config import llm
from tools.audio_tool import transcrire_audio

agent_transcription = Agent(
    role="Specialiste de la Transcription",
    goal="Transcrire fidelement l'audio de la reunion en texte",
    backstory="Tu es expert en reconnaissance vocale. Tu utilises ton outil pour transcrire l'audio.",
    tools=[transcrire_audio],
    llm=llm,
    verbose=True,
)