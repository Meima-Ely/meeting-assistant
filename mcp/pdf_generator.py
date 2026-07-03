from fpdf import FPDF
from datetime import datetime
import os


def generer_pdf(resume, analyse, nom_fichier="compte_rendu.pdf"):
    """Genere un PDF professionnel du compte-rendu de reunion."""
    pdf = FPDF()
    pdf.add_page()

    # Couleur d'accent (bleu)
    bleu = (41, 98, 168)

    # === TITRE ===
    pdf.set_fill_color(*bleu)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 18, "COMPTE-RENDU DE REUNION", ln=True, align="C", fill=True)

    # Date
    pdf.set_text_color(100, 100, 100)
    pdf.set_font("Helvetica", "I", 11)
    date_str = datetime.now().strftime("%d/%m/%Y a %H:%M")
    pdf.cell(0, 10, f"Genere le {date_str}", ln=True, align="C")
    pdf.ln(5)

    # === RESUME EXECUTIF ===
    pdf.set_text_color(*bleu)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "RESUME EXECUTIF", ln=True)
    pdf.set_draw_color(*bleu)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_text_color(30, 30, 30)
    pdf.set_font("Helvetica", "", 11)
    # Nettoyer le texte pour eviter les caracteres non supportes
    resume_clean = resume.encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, 7, resume_clean)
    pdf.ln(5)

    # === ANALYSE DETAILLEE ===
    pdf.set_text_color(*bleu)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "ANALYSE DETAILLEE", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_text_color(30, 30, 30)
    pdf.set_font("Helvetica", "", 11)
    analyse_clean = analyse.encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, 7, analyse_clean)

    # === PIED DE PAGE ===
    pdf.ln(10)
    pdf.set_text_color(150, 150, 150)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 8, "Genere automatiquement par l'Assistant Intelligent de Reunion", ln=True, align="C")

    # Sauvegarder
    chemin = os.path.join("uploads_temp", nom_fichier)
    os.makedirs("uploads_temp", exist_ok=True)
    pdf.output(chemin)
    return chemin