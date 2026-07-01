import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("GITHUB_TOKEN")
repo = os.environ.get("GITHUB_REPO")

url = f"https://api.github.com/repos/{repo}/issues"
print("URL appelee :", repr(url))   # repr montre les espaces caches

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github+json",
}
data = {"title": "Test direct", "body": "Test"}

r = requests.post(url, headers=headers, json=data)
print("Status :", r.status_code)
print("Reponse :", r.text[:300])