import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def envoyer_notification(message):
    """Envoie un message Telegram. Retourne True si reussi."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return True
    else:
        print(f"Erreur Telegram {response.status_code} : {response.text}")
        return False
def notifier_taches_creees(issues, repo):
    """Construit et envoie une notification Telegram des taches creees."""
    nb = len(issues)
    liste_taches = ""
    for i, issue in enumerate(issues, 1):
        liste_taches += f"  {i}. {issue['tache']} ({issue['responsable']})\n"

    message = (
        f"🎙️ *ASSISTANT DE REUNION*\n"
        f"━━━━━━━━━━━━━━━\n\n"
        f"✅ *Reunion analysee avec succes !*\n\n"
        f"📋 *{nb} taches creees sur GitHub :*\n"
        f"{liste_taches}\n"
        f"🔗 [Voir les taches](https://github.com/{repo}/issues)\n\n"
        f"_Genere par votre assistant IA_ 🤖"
    )
    return envoyer_notification(message)