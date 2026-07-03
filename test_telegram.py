from mcp.telegram_connector import envoyer_notification

resultat = envoyer_notification("Test - est-ce que tu recois ce message ?")
print("Resultat envoi :", resultat)