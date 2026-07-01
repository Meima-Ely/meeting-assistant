import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("GITHUB_TOKEN")

r = requests.get("https://api.github.com/user",
                 headers={"Authorization": f"token {token}"})

# Les scopes du token sont dans les headers de la reponse
print("Scopes du token :", r.headers.get("X-OAuth-Scopes", "AUCUN"))