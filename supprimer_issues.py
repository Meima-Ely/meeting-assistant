import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("GITHUB_TOKEN")
REPO = os.environ.get("GITHUB_REPO")

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json",
}

# 1. Recuperer toutes les issues (ouvertes ET fermees)
url = f"https://api.github.com/repos/{REPO}/issues?state=all&per_page=100"
issues = requests.get(url, headers=headers).json()

print(f"{len(issues)} issues trouvees.")

# 2. Pour chaque issue, recuperer son node_id (necessaire pour la suppression GraphQL)
for issue in issues:
    numero = issue["number"]
    node_id = issue["node_id"]

    # La suppression se fait via GraphQL (l'API REST ne permet pas de supprimer)
    query = """
    mutation($id: ID!) {
      deleteIssue(input: {issueId: $id}) {
        clientMutationId
      }
    }
    """
    r = requests.post(
        "https://api.github.com/graphql",
        headers=headers,
        json={"query": query, "variables": {"id": node_id}},
    )
    if r.status_code == 200 and "errors" not in r.json():
        print(f"✅ Issue #{numero} supprimee")
    else:
        print(f"❌ Issue #{numero} : {r.json()}")

print("Termine !")