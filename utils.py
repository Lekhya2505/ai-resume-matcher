import PyPDF2
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_pdf_report(data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(50, 750, "AI Resume vs Job Description Report")
    c.drawString(50, 730, f"Overall Match Score: {data['score']}%")

    y = 710
    c.drawString(50, y, "Section-wise Match:")
    for section, score in data["section_scores"].items():
        y -= 20
        c.drawString(70, y, f"{section}: {score}%")

    y -= 40
    c.drawString(50, y, "Suggestions:")
    y -= 20
    c.drawString(70, y, data["suggestions"][:100])  # trim long strings

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
