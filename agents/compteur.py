import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def compter_elements(texte_analyse):
    """Demande au LLM de compter precisement les elements de l'analyse.
    Retourne un dict : {decisions, taches, echeances, blocages}."""
    prompt = f"""Analyse ce compte-rendu de reunion et compte PRECISEMENT le nombre de :
- decisions prises
- taches assignees
- echeances (dates limites distinctes, ne compte pas deux fois la meme date)
- points de blocage

Reponds UNIQUEMENT avec un objet JSON valide, rien d'autre, au format exact :
{{"decisions": 0, "taches": 0, "echeances": 0, "blocages": 0}}

Compte-rendu :
{texte_analyse}

JSON :"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    texte = response.choices[0].message.content.strip()
    texte = texte.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(texte)
        return {
            "decisions": int(data.get("decisions", 0)),
            "taches": int(data.get("taches", 0)),
            "echeances": int(data.get("echeances", 0)),
            "blocages": int(data.get("blocages", 0)),
        }
    except Exception as e:
        print(f"Erreur comptage : {e}")
        return {"decisions": 0, "taches": 0, "echeances": 0, "blocages": 0}