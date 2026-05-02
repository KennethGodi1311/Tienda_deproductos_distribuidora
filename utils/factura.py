from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


def generar_factura(carrito, total):
    """
    Genera un archivo PDF con la factura de compra.

    Parámetros:
    - carrito: lista de productos (dict con producto, precio, cantidad)
    - total: monto total de la compra
    """

    # -------------------------
    # VALIDACIÓN
    # -------------------------
    if not carrito:
        return

    # -------------------------
    # DOCUMENTO
    # -------------------------
    doc = SimpleDocTemplate("factura.pdf")
    styles = getSampleStyleSheet()

    contenido = []

    # -------------------------
    # HEADER
    # -------------------------
    contenido.append(Paragraph("🐉 Pulpería El Dragón Dorado", styles["Title"]))
    contenido.append(Spacer(1, 10))

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    contenido.append(Paragraph(f"Fecha: {fecha}", styles["Normal"]))
    contenido.append(Spacer(1, 10))

    contenido.append(Paragraph("----------------------------------------", styles["Normal"]))
    contenido.append(Spacer(1, 5))

    # -------------------------
    # DETALLE PRODUCTOS
    # -------------------------
    for item in carrito:
        producto = item.get("producto", "N/A")
        cantidad = item.get("cantidad", 0)
        precio = item.get("precio", 0)

        subtotal = precio * cantidad

        texto = f"{producto} x{cantidad} → ₡{subtotal}"
        contenido.append(Paragraph(texto, styles["Normal"]))
        contenido.append(Spacer(1, 5))

    # -------------------------
    # TOTAL
    # -------------------------
    contenido.append(Spacer(1, 10))
    contenido.append(Paragraph("----------------------------------------", styles["Normal"]))
    contenido.append(Spacer(1, 5))

    contenido.append(Paragraph(f"TOTAL: ₡{total}", styles["Heading2"]))

    contenido.append(Spacer(1, 15))

    # -------------------------
    # FOOTER
    # -------------------------
    contenido.append(Paragraph("¡Gracias por su compra!", styles["Normal"]))
    contenido.append(Paragraph("Vuelva pronto 🛒", styles["Normal"]))

    # -------------------------
    # GENERAR PDF
    # -------------------------
    doc.build(contenido)