from mcp.github_connector import creer_issue

resultat = creer_issue(
    "Test - Tache depuis reunion",
    "Ceci est un test du connecteur MCP GitHub."
)
print("Resultat :", resultat)