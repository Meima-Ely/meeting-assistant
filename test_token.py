import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("GITHUB_TOKEN")
repo = os.environ.get("GITHUB_REPO")

print("Token commence par :", token[:7] if token else "VIDE")
print("Repo lu :", repo)
print("-" * 40)

# Test 1 : token valide ?
r = requests.get("https://api.github.com/user",
                 headers={"Authorization": f"token {token}"})
print("Test token :", r.status_code)
if r.status_code == 200:
    print("  Connecte en tant que :", r.json()["login"])

# Test 2 : acces au repo ?
r2 = requests.get(f"https://api.github.com/repos/{repo}",
                  headers={"Authorization": f"token {token}"})
print("Test repo :", r2.status_code)