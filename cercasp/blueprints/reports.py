from flask import Blueprint, send_file
from flask_login import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
import io
import pandas as pd
from ..models import Intern
from flask_babel import _

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/pdf')
@login_required
def generate_pdf_report():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph(_("Reporte Completo de Internos"), styles['Title']))
    story.append(Spacer(1, 12))
    # Example table
    data = [['ID', 'Nombre', 'Edad']]
    for i in Intern.query.all():
        data.append([i.id, i.name, i.age])
    table = Table(data)
    story.append(table)
    # Example image
    img_path = 'static/images/logo.png'  # Assume exists
    story.append(Image(img_path, width=100, height=100))
    doc.build(story)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='report.pdf', mimetype='application/pdf')

@reports_bp.route('/export_interns')
@login_required
def export_interns():
    interns = Intern.query.all()
    data = [{'ID': i.id, 'Nombre': i.name, 'Edad': i.age, 'Género': i.gender} for i in interns]
    df = pd.DataFrame(data)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    return send_file(io.BytesIO(csv_buffer.getvalue().encode()), as_attachment=True, download_name='interns.csv', mimetype='text/csv')
