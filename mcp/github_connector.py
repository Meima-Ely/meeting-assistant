import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO")


def creer_issue(titre, description=""):
    """Cree une issue GitHub. Retourne l'URL de l'issue creee."""
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
        return f"Erreur {response.status_code} : {response.text}"