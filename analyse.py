import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Le texte transcrit (pour l'instant on le met a la main pour tester)
transcription = """
Bonjour, ceci est un test de transcription. On decide de livrer le projet vendredi.
Brahim s'occupe de la base de donnees. Moi je prends l'interface utilisateur.
Il y a un blocage : on attend l'acces au serveur. Le rapport, on le prepare lundi.
"""

# Le prompt : on demande au LLM d'extraire en JSON
prompt = f"""Tu es un assistant qui analyse des reunions.
A partir de la transcription ci-dessous, extrais les informations en JSON.

Transcription :
{transcription}

Reponds UNIQUEMENT avec un JSON valide, sans texte avant ni apres, dans ce format exact :
{{
  "decisions": ["..."],
  "taches": [{{"tache": "...", "responsable": "..."}}],
  "echeances": ["..."],
  "points_de_blocage": ["..."]
}}
"""

print("Analyse en cours...\n")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    temperature=0,
)

resultat = response.choices[0].message.content

# Nettoyer et parser le JSON
resultat = resultat.replace("```json", "").replace("```", "").strip()
data = json.loads(resultat)

# Afficher proprement
print("=" * 50)
print("DECISIONS :")
for d in data["decisions"]:
    print(f"  - {d}")

print("\nTACHES :")
for t in data["taches"]:
    print(f"  - {t['tache']} (responsable : {t['responsable']})")

print("\nECHEANCES :")
for e in data["echeances"]:
    print(f"  - {e}")

print("\nPOINTS DE BLOCAGE :")
for b in data["points_de_blocage"]:
    print(f"  - {b}")
print("=" * 50)
print("\nTermine !")