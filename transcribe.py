import subprocess
from faster_whisper import WhisperModel

# 1. MP4 -> audio WAV 16kHz mono (FFmpeg jette la video, garde le son)
print("Extraction de l'audio...")
subprocess.run([
    "ffmpeg", "-i", "reunion.mp4",
    "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
    "audio.wav", "-y"
], check=True)

# 2. Charger le modele Whisper (local, gratuit)
print("Chargement du modele Whisper...")
model = WhisperModel("small", device="cpu", compute_type="int8")

# 3. Transcrire
print("Transcription en cours...\n")
segments, info = model.transcribe("audio.wav", language="fr")

print(f"Langue detectee : {info.language}\n")
print("=" * 50)
for seg in segments:
    print(f"[{seg.start:.1f}s -> {seg.end:.1f}s] {seg.text}")
print("=" * 50)
print("\nTermine !")