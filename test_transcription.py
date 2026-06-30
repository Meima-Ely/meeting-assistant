import subprocess
from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Adapte le nom si besoin
FICHIER = "FRENCAIS.mp4"

print("Extraction audio...")
subprocess.run([
    "ffmpeg", "-i", FICHIER,
    "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
    "audio_test.wav", "-y"
], check=True, capture_output=True)

print("Transcription...\n")
with open("audio_test.wav", "rb") as f:
    audio_data = f.read()

transcription = client.audio.transcriptions.create(
    file=("audio_test.wav", audio_data),
    model="whisper-large-v3-turbo",
    response_format="text",
    language="fr",
)

print("=" * 60)
print("TRANSCRIPTION BRUTE :")
print("=" * 60)
print(transcription)