from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import os


def generar_pdf(orders, clients, rutas):
    # Crear carpeta temporal si no existe
    os.makedirs("temp", exist_ok=True)
    ruta_salida = "temp/informe_drones.pdf"

    # Crear canvas
    c = canvas.Canvas(ruta_salida, pagesize=letter)
    width, height = letter
    y = height - 50

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "📄 Informe de Entregas de Drones")
    y -= 30

    # Resumen general
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Total Órdenes entregadas: {len(orders)}")
    y -= 20
    c.drawString(50, y, f"Total Clientes registrados: {len(clients)}")
    y -= 20
    c.drawString(50, y, f"Total Rutas únicas usadas: {len(rutas)}")
    y -= 30

    # Sección: Clientes
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "👥 Clientes:")
    y -= 20
    for client in clients[:5]:  # Limitar a los primeros 5
        tipo = client.get("type", "normal")
        nombre = client.get("name", "Desconocido")
        c.setFont("Helvetica", 11)
        c.drawString(60, y, f"- {nombre} ({tipo})")
        y -= 15
        if y < 100:
            c.showPage()
            y = height - 50

    y -= 20

    # Sección: Órdenes
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "📦 Órdenes (primeras 5):")
    y -= 20

    headers = ["ID", "Origen", "Destino", "Costo", "Entregado"]
    data = [headers]

    for order in orders[:5]:
        data.append([
            order.get("order_id"),
            order.get("origin"),
            order.get("destination"),
            order.get("cost"),
            "✔️" if order.get("delivered_at") else "❌"
        ])

    table = Table(data, colWidths=[80, 80, 80, 60, 60])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

    table.wrapOn(c, width, y)
    table.drawOn(c, 50, y - 100)
    y -= 140

    # Sección: Rutas frecuentes
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "🛣️ Rutas frecuentes:")
    y -= 20

    for i, (ruta, freq) in enumerate(rutas[:5], start=1):
        c.setFont("Helvetica", 11)
        c.drawString(60, y, f"{i}. {ruta} (x{freq})")
        y -= 15
        if y < 100:
            c.showPage()
            y = height - 50

    # Finalizar PDF
    c.save()
    return ruta_salida
