from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from datetime import datetime
import os
import sqlite3
import qrcode


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


def generar_qr(texto):
    qr = qrcode.make(texto)
    ruta = "qr.png"
    qr.save(ruta)
    return ruta


def generar_factura(carrito, total, metodo_pago):

    if not carrito:
        return

    # -------------------------
    # CONFIG
    # -------------------------
    doc = SimpleDocTemplate("factura.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    contenido = []

    # -------------------------
    # DATOS EMPRESA
    # -------------------------
    empresa = "Pulpería El Dragón Dorado"
    cedula = "3-101-999999"
    direccion = "Barrio Chino, San José"
    telefono = "2230-5698"

    numero_factura = generar_numero_factura()
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    # -------------------------
    # LOGO (opcional)
    # -------------------------
    if os.path.exists("logo.png"):
        contenido.append(Image("logo.png", width=1.5*inch, height=1.5*inch))

    contenido.append(Paragraph(f"<b>{empresa}</b>", styles["Title"]))
    contenido.append(Paragraph(f"Cédula: {cedula}", styles["Normal"]))
    contenido.append(Paragraph(f"{direccion}", styles["Normal"]))
    contenido.append(Paragraph(f"Tel: {telefono}", styles["Normal"]))
    contenido.append(Spacer(1, 10))

    contenido.append(Paragraph(f"<b>Factura:</b> {numero_factura}", styles["Normal"]))
    contenido.append(Paragraph(f"Fecha: {fecha}", styles["Normal"]))
    contenido.append(Paragraph(f"Método de pago: {metodo_pago}", styles["Normal"]))

    contenido.append(Spacer(1, 15))

    # -------------------------
    # TABLA PRODUCTOS
    # -------------------------
    data = [["Producto", "Cantidad", "Precio", "Total"]]

    subtotal = 0

    for item in carrito:
        producto = item["producto"]
        cantidad = item["cantidad"]
        precio = item["precio"]

        total_linea = cantidad * precio
        subtotal += total_linea

        data.append([
            producto,
            str(cantidad),
            f"₡{precio}",
            f"₡{total_linea}"
        ])

    tabla = Table(data)

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.black),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
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
    contenido.append(Paragraph(f"<b>Total: ₡{round(total_final,2)}</b>", styles["Heading2"]))

    contenido.append(Spacer(1, 20))

    # -------------------------
    # QR
    # -------------------------
    texto_qr = f"Factura {numero_factura} - Total ₡{round(total_final,2)}"
    ruta_qr = generar_qr(texto_qr)

    contenido.append(Image(ruta_qr, width=1.5*inch, height=1.5*inch))

    contenido.append(Spacer(1, 10))

    # -------------------------
    # LEYENDA LEGAL
    # -------------------------
    contenido.append(Paragraph(
        "Este documento es una representación gráfica de una factura electrónica.",
        styles["Normal"]
    ))

    contenido.append(Paragraph(
        "No válido ante el Ministerio de Hacienda sin firma digital.",
        styles["Normal"]
    ))

    contenido.append(Spacer(1, 10))
    contenido.append(Paragraph("Gracias por su compra", styles["Normal"]))

    # -------------------------
    # GENERAR PDF
    # -------------------------
    doc.build(contenido)