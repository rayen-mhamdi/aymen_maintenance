from jinja2 import Environment, FileSystemLoader
from django.http import FileResponse
from xhtml2pdf import pisa
from io import BytesIO
import os
from pathlib import Path
from django.shortcuts import render

def generate_pdf(request, queryset):
    if queryset.count() > 1:
        return render(request, '500.html', {'exception': "Il faut selectionné un seul Récu"}, status=500)
    
    base_path = os.path.join(Path(__file__).resolve().parent.parent, "templates")
    env = Environment(loader=FileSystemLoader(base_path))
    template = env.get_template('ticket.html')
    html_content = template.render(data=queryset)

    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(html_content, pdf)

    if pisa_status.err:
        raise Exception("Error creating PDF")

    pdf.seek(0)
    return pdf
