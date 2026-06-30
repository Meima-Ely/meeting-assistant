import subprocess
from crewai.tools import tool
from config import groq_client

@tool("Transcripteur Audio")
def transcrire_audio(fichier_mp4: str) -> str:
    """Extrait l'audio d'un MP4 et le transcrit en texte avec Whisper via Groq.
    Prend le chemin du MP4 et retourne le texte transcrit."""
    subprocess.run([
        "ffmpeg", "-i", fichier_mp4,
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
        "audio.wav", "-y"
    ], check=True, capture_output=True)
    with open("audio.wav", "rb") as f:
        audio_data = f.read()
    transcription = groq_client.audio.transcriptions.create(
        file=("audio.wav", audio_data),
        model="whisper-large-v3-turbo",
        response_format="text",
        language="fr",
    )
    return str(transcription)