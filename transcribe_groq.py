import os
import subprocess
from dotenv import load_dotenv
from groq import Groq

# Charger la cle depuis .env
load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# 1. MP4 -> audio WAV 16kHz mono
print("Extraction de l'audio...")
subprocess.run([
    "ffmpeg", "-i", "reunion.mp4",
    "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
    "audio.wav", "-y"
], check=True, capture_output=True)

# 2. Envoyer a Groq (Whisper rapide)
print("Transcription via Groq...\n")
with open("audio.wav", "rb") as f:
    audio_data = f.read()

transcription = client.audio.transcriptions.create(
    file=("audio.wav", audio_data),
    model="whisper-large-v3-turbo",
    response_format="verbose_json",
    language="fr",
)

# 3. Afficher
print("=" * 50)
for seg in transcription.segments:
    start = seg["start"] if isinstance(seg, dict) else seg.start
    end = seg["end"] if isinstance(seg, dict) else seg.end
    text = seg["text"] if isinstance(seg, dict) else seg.text
    print(f"[{start:.1f}s -> {end:.1f}s] {text}")
print("=" * 50)
print("\nTexte complet :\n")
print(transcription.text)
print("\nTermine !")