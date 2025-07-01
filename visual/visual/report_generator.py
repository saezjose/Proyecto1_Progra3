from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import os

def generar_pdf(orders, clients, rutas, filename="informe_drones.pdf"):
    ruta_archivo = os.path.join("temp", filename)
    os.makedirs("temp", exist_ok=True)

    c = canvas.Canvas(ruta_archivo, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "📄 Informe del Sistema Logístico de Drones")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    y = height - 100
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "📋 Clientes más recurrentes:")
    y -= 20
    c.setFont("Helvetica", 10)

    top_clients = sorted(clients, key=lambda x: x["total_orders"], reverse=True)[:5]
    for cli in top_clients:
        c.drawString(60, y, f"{cli['id']} - {cli['name']} | Pedidos: {cli['total_orders']}")
        y -= 15

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "📦 Órdenes registradas:")
    y -= 20
    c.setFont("Helvetica", 10)

    for order in orders[:10]:  # Mostrar solo las 10 primeras
        text = f"{order['order_id']} - {order['origin']} → {order['destination']} | Costo: {order['route_cost']} | Estado: {order['status']}"
        c.drawString(60, y, text)
        y -= 12
        if y < 80:
            c.showPage()
            y = height - 80

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "📍 Rutas más frecuentes:")
    y -= 20
    c.setFont("Helvetica", 10)

    for ruta, freq in rutas[:10]:
        c.drawString(60, y, f"{ruta} | Veces: {freq}")
        y -= 12
        if y < 80:
            c.showPage()
            y = height - 80

    c.showPage()
    c.save()

    return ruta_archivo
