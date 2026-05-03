from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from datetime import datetime
import os
import sqlite3

# 🔥 IMPORT SEGURO (NO ROMPE SI NO EXISTE)
try:
    import qrcode
    QR_AVAILABLE = True
except:
    QR_AVAILABLE = False


# =========================
# GENERAR NÚMERO FACTURA REAL
# =========================
def generar_numero_factura():
    conn = sqlite3.connect("tienda.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT
    )
    """)

    cursor.execute("INSERT INTO facturas DEFAULT VALUES")
    conn.commit()

    numero = cursor.lastrowid
    conn.close()

    return f"FAC-{numero:06d}"


# =========================
# GENERAR QR (SEGURO)
# =========================
def generar_qr(texto):
    if not QR_AVAILABLE:
        return None

    ruta = "qr_temp.png"

    qr = qrcode.make(texto)
    qr.save(ruta)

    return ruta


# =========================
# FACTURA PRINCIPAL
# =========================
def generar_factura(carrito, total, metodo_pago):

    if not carrito:
        return

    doc = SimpleDocTemplate("factura.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    contenido = []

    # -------------------------
    # DATOS EMPRESA
    # -------------------------
    empresa = "Pulpería El Dragón Dorado"
    cedula = "3-101-999999"
    direccion = "Barrio Chino, San José, Costa Rica"
    telefono = "2230-5698"

    numero_factura = generar_numero_factura()
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    # -------------------------
    # HEADER
    # -------------------------
    if os.path.exists("logo.png"):
        contenido.append(Image("logo.png", width=1.2*inch, height=1.2*inch))

    contenido.append(Paragraph(f"<b>{empresa}</b>", styles["Title"]))
    contenido.append(Paragraph(f"Cédula Jurídica: {cedula}", styles["Normal"]))
    contenido.append(Paragraph(direccion, styles["Normal"]))
    contenido.append(Paragraph(f"Tel: {telefono}", styles["Normal"]))
    contenido.append(Spacer(1, 10))

    contenido.append(Paragraph(f"<b>Factura N°:</b> {numero_factura}", styles["Normal"]))
    contenido.append(Paragraph(f"Fecha: {fecha}", styles["Normal"]))
    contenido.append(Paragraph(f"Método de pago: {metodo_pago}", styles["Normal"]))

    contenido.append(Spacer(1, 15))

    # -------------------------
    # TABLA PRODUCTOS
    # -------------------------
    data = [["Producto", "Cant.", "Precio", "Total"]]

    subtotal = 0

    for item in carrito:
        producto = item["producto"]
        cantidad = item["cantidad"]
        precio = item["precio"]

        total_linea = cantidad * precio
        subtotal += total_linea

        data.append([
            producto.capitalize(),
            str(cantidad),
            f"₡{precio}",
            f"₡{total_linea}"
        ])

    tabla = Table(data, hAlign='LEFT')

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

    contenido.append(tabla)

    # -------------------------
    # TOTALES
    # -------------------------
    iva = subtotal * 0.13
    total_final = subtotal + iva

    contenido.append(Spacer(1, 15))

    contenido.append(Paragraph(f"Subtotal: ₡{round(subtotal,2)}", styles["Normal"]))
    contenido.append(Paragraph(f"IVA (13%): ₡{round(iva,2)}", styles["Normal"]))
    contenido.append(Paragraph(f"<b>TOTAL: ₡{round(total_final,2)}</b>", styles["Heading2"]))

    contenido.append(Spacer(1, 20))

    # -------------------------
    # QR (SI EXISTE LIBRERÍA)
    # -------------------------
    ruta_qr = generar_qr(f"{numero_factura} | ₡{round(total_final,2)}")

    if ruta_qr and os.path.exists(ruta_qr):
        contenido.append(Image(ruta_qr, width=1.5*inch, height=1.5*inch))

    contenido.append(Spacer(1, 10))

    # -------------------------
    # LEYENDA LEGAL (CR)
    # -------------------------
    contenido.append(Paragraph(
        "Documento conforme a la normativa tributaria vigente en Costa Rica.",
        styles["Normal"]
    ))

    contenido.append(Paragraph(
        "Representación gráfica de comprobante electrónico.",
        styles["Normal"]
    ))

    contenido.append(Paragraph(
        "Para efectos fiscales, debe contar con validación del Ministerio de Hacienda.",
        styles["Normal"]
    ))

    contenido.append(Spacer(1, 10))
    contenido.append(Paragraph("Gracias por su compra", styles["Normal"]))

    # -------------------------
    # GENERAR PDF
    # -------------------------
    doc.build(contenido)

    # 🧹 LIMPIAR QR TEMPORAL
    if ruta_qr and os.path.exists(ruta_qr):
        os.remove(ruta_qr)