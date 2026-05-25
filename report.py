from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
import io

def generate_pdf(title: str, content: str) -> bytes:
    """Convert markdown report into a downloadable PDF."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=inch, leftMargin=inch,
        topMargin=inch, bottomMargin=inch
    )

    styles = getSampleStyleSheet()
    title_style  = ParagraphStyle('T', parent=styles['Title'],   fontSize=20, spaceAfter=20)
    h1_style     = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=16, spaceAfter=10)
    h2_style     = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=13, spaceAfter=8)
    body_style   = ParagraphStyle('B', parent=styles['Normal'],  fontSize=11, leading=17)
    bullet_style = ParagraphStyle('BL', parent=styles['Normal'], fontSize=11, leading=17, leftIndent=20)

    story = [Paragraph(title, title_style), Spacer(1, 0.2 * inch)]

    for line in content.split('\n'):
        line = line.strip()
        if not line:
            story.append(Spacer(1, 0.08 * inch))
        elif line.startswith('# '):
            story.append(Paragraph(line[2:], h1_style))
        elif line.startswith('## '):
            story.append(Paragraph(line[3:], h2_style))
        elif line.startswith('- ') or line.startswith('* '):
            story.append(Paragraph(f"• {line[2:]}", bullet_style))
        else:
            story.append(Paragraph(line, body_style))

    doc.build(story)
    return buffer.getvalue()