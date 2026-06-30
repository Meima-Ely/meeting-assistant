from rag_memory import memoriser_reunion, poser_question

# 1. On memorise une reunion (texte de test)
texte_reunion = """
Reunion du 30 juin. On decide que la livraison finale du projet sera le 11 juillet.
La demo client aura lieu le 14 juillet. Brahim s'occupe de la base de donnees,
a terminer avant mercredi. Fatima est responsable du rapport final pour le 9 juillet.
On augmente le budget de 2000 dollars pour un nouveau serveur.
Blocage : on attend l'acces API du client. Karim va le contacter aujourd'hui.
"""

print("=== MEMORISATION ===")
resultat = memoriser_reunion(texte_reunion, "reunion_30juin")
print(resultat)

# 2. On pose des questions
print("\n=== QUESTIONS ===\n")

questions = [
    "Qui s'occupe de la base de donnees ?",
    "Quel est le budget ?",
    "Quelles sont les echeances ?",
    "Y a-t-il des blocages ?",
]

for q in questions:
    print(f"Q : {q}")
    reponse = poser_question(q)
    print(f"R : {reponse}\n")