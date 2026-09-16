import os
import requests
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO")
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def creer_issue(titre, description=""):
    """Cree une issue GitHub. Retourne l'URL de l'issue creee, ou None en cas d'echec."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    data = {"title": titre, "body": description}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()["html_url"]
    else:
        print(f"Erreur GitHub {response.status_code} : {response.text}")
        return None


def extraire_taches(texte_analyse):
    """Utilise le LLM pour extraire une liste propre de taches (une par responsable)."""
    prompt = f"""Voici l'analyse d'une reunion. Extrais les taches PRINCIPALES a faire.

REGLES IMPORTANTES :
- Regroupe les taches d'une MEME personne en UNE SEULE tache (ex: si Karim doit "gerer l'integration" ET "contacter le client", cree une seule tache "Gerer l'integration et contacter le client").
- N'inclus PAS les points de blocage comme des taches (ex: "obtenir l'acces aux donnees", "remplacer le serveur" sont des blocages, PAS des taches assignees).
- Si deux noms se ressemblent (Karim/Kerim), traite-les comme la meme personne.
- Vise idealement UNE tache par personne responsable.
- Maximum 6 taches.

Reponds avec une tache par ligne, au format exact : Tache | Responsable
Si pas de responsable identifie, mets "Non specifie".
N'ajoute AUCUN autre texte, juste les lignes.

Analyse :
{texte_analyse}

Taches :"""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    texte = response.choices[0].message.content.strip()

    taches = []
    for ligne in texte.split("\n"):
        ligne = ligne.strip()
        if "|" in ligne:
            parts = ligne.split("|")
            tache = parts[0].strip("- ").strip()
            responsable = parts[1].strip() if len(parts) > 1 else "Non specifie"
            if tache:
                taches.append({"tache": tache, "responsable": responsable})
    return taches


def creer_issues_depuis_analyse(texte_analyse):
    """Extrait les taches de l'analyse et cree une issue GitHub pour chacune."""
    taches = extraire_taches(texte_analyse)
    resultats = []
    for t in taches:
        titre = t["tache"]
        description = (
            f"**Responsable :** {t['responsable']}\n\n"
            f"_Tache extraite automatiquement d'une reunion par l'assistant IA._"
        )
        url = creer_issue(titre, description)
        resultats.append({"tache": titre, "responsable": t["responsable"], "url": url})
    return resultats
