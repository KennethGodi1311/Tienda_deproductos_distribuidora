from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

def generar_factura(producto, precio):

    doc = SimpleDocTemplate("factura.pdf")
    styles = getSampleStyleSheet()

    contenido = [
        Paragraph("Pulpería El Dragón Dorado", styles["Title"]),
        Paragraph(f"Producto: {producto}", styles["Normal"]),
        Paragraph(f"Precio: ₡{precio}", styles["Normal"]),
        Paragraph(f"Fecha: {datetime.now()}", styles["Normal"]),
    ]

    doc.build(contenido)