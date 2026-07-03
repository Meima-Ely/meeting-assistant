from fpdf import FPDF
from datetime import datetime
import os
import re


# Couleurs (RGB)
BLEU = (46, 111, 237)
BLEU_CLAIR = (232, 240, 253)
GRIS_FONCE = (30, 41, 59)
GRIS = (100, 116, 139)
VERT = (34, 197, 94)
VERT_CLAIR = (236, 253, 245)
ORANGE = (245, 158, 11)
ORANGE_CLAIR = (255, 251, 235)
ROUGE = (239, 68, 68)
ROUGE_CLAIR = (255, 241, 242)
VIOLET = (139, 92, 246)
VIOLET_CLAIR = (245, 243, 255)


def _clean(texte):
    """Nettoie le texte pour le rendu PDF (accents geres, caracteres speciaux remplaces)."""
    remplacements = {
        "\u0153": "oe", "\u0152": "OE",  # oe
        "\u2019": "'", "\u2018": "'",     # apostrophes
        "\u201c": '"', "\u201d": '"',     # guillemets
        "\u2013": "-", "\u2014": "-",     # tirets
        "\u2026": "...",                  # points de suspension
        "\u2192": "->",                   # fleche
    }
    for k, v in remplacements.items():
        texte = texte.replace(k, v)
    # Enlever les emojis et symboles non latin-1
    texte = texte.encode("latin-1", "ignore").decode("latin-1")
    return texte


def _extraire_sections(analyse):
    """Parse l'analyse structuree en 4 listes : decisions, taches, echeances, blocages."""
    sections = {"decisions": [], "taches": [], "echeances": [], "blocages": []}
    courant = None
    for ligne in analyse.split("\n"):
        l = ligne.strip()
        if not l:
            continue
        bas = l.lower()
        # Detecter les en-tetes de section
        if "décision" in bas or "decision" in bas:
            if l.startswith("**") or ":" in l and len(l) < 40:
                courant = "decisions"
                continue
        if "tâche" in bas or "tache" in bas:
            if l.startswith("**") or (":" in l and len(l) < 40):
                courant = "taches"
                continue
        if "échéance" in bas or "echeance" in bas:
            if l.startswith("**") or (":" in l and len(l) < 40):
                courant = "echeances"
                continue
        if "blocage" in bas:
            if l.startswith("**") or (":" in l and len(l) < 40):
                courant = "blocages"
                continue
        # Ligne de contenu (numerotee ou avec tiret)
        if courant and re.match(r"^(\d+\.|\-|\*|•)", l):
            item = re.sub(r"^(\d+\.|\-|\*|•)\s*", "", l).strip()
            item = item.replace("**", "")
            if item:
                sections[courant].append(item)
    return sections


class PDF(FPDF):
    def header(self):
        # Bande coloree en haut
        self.set_fill_color(*BLEU)
        self.rect(0, 0, 210, 32, "F")
        self.set_y(9)
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, "COMPTE-RENDU DE REUNION", ln=True, align="C")
        self.set_font("Helvetica", "", 10)
        date_str = datetime.now().strftime("%d/%m/%Y a %H:%M")
        self.cell(0, 6, f"Genere le {date_str}", ln=True, align="C")
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRIS)
        self.cell(0, 10, "Genere automatiquement par l'Assistant Intelligent de Reunion - PFE", align="C")

    def section_titre(self, texte, couleur, couleur_claire):
        self.ln(3)
        self.set_fill_color(*couleur_claire)
        self.set_text_color(*couleur)
        self.set_font("Helvetica", "B", 13)
        self.cell(0, 10, f"  {_clean(texte)}", ln=True, fill=True)
        self.ln(2)

    def bloc_texte(self, texte):
        self.set_text_color(*GRIS_FONCE)
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 6, _clean(texte))
        self.ln(1)

    def liste_items(self, items, couleur):
        self.set_font("Helvetica", "", 10.5)
        for item in items:
            # Puce coloree
            y = self.get_y()
            self.set_fill_color(*couleur)
            self.ellipse(12, y + 2, 2, 2, "F")
            self.set_x(17)
            self.set_text_color(*GRIS_FONCE)
            self.multi_cell(0, 6, _clean(item))
            self.ln(0.5)


def generer_pdf(resume, analyse, nom_fichier="compte_rendu.pdf"):
    """Genere un PDF professionnel et attractif du compte-rendu de reunion."""
    pdf = PDF()
    pdf.add_page()

    # ===== RESUME EXECUTIF =====
    pdf.section_titre("RESUME EXECUTIF", BLEU, BLEU_CLAIR)
    pdf.bloc_texte(resume)

    # ===== SECTIONS DETAILLEES =====
    sections = _extraire_sections(analyse)

    if sections["decisions"]:
        pdf.section_titre("DECISIONS PRISES", VIOLET, VIOLET_CLAIR)
        pdf.liste_items(sections["decisions"], VIOLET)

    if sections["taches"]:
        pdf.section_titre("TACHES ET RESPONSABLES", BLEU, BLEU_CLAIR)
        pdf.liste_items(sections["taches"], BLEU)

    if sections["echeances"]:
        pdf.section_titre("ECHEANCES", ORANGE, ORANGE_CLAIR)
        pdf.liste_items(sections["echeances"], ORANGE)

    if sections["blocages"]:
        pdf.section_titre("POINTS DE BLOCAGE", ROUGE, ROUGE_CLAIR)
        pdf.liste_items(sections["blocages"], ROUGE)

    # Si le parsing n'a rien trouve, afficher l'analyse brute
    if not any(sections.values()):
        pdf.section_titre("ANALYSE DETAILLEE", BLEU, BLEU_CLAIR)
        pdf.bloc_texte(analyse)

    # Sauvegarder
    os.makedirs("uploads_temp", exist_ok=True)
    chemin = os.path.join("uploads_temp", nom_fichier)
    pdf.output(chemin)
    return chemin