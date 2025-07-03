from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import Image

# -----------------------------
# Función para guardar los gráficos como PNG
# -----------------------------
import matplotlib.pyplot as plt
import pandas as pd
import os

def guardar_graficos_pdf(graph, sim):
    os.makedirs("temp", exist_ok=True)

    # === Pie Chart: Distribución de nodos ===
    roles = {"📦": "Storage", "🔋": "Recharge", "👤": "Clients"}
    role_counts = {k: 0 for k in roles}
    for v in graph.vertices():
        for symbol in roles:
            if str(v).startswith(symbol):
                role_counts[symbol] += 1

    labels = [roles[k] for k in role_counts]
    sizes = [role_counts[k] for k in role_counts]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")
    plt.title("Distribución de Nodos")
    plt.savefig("temp/nodos_pie_chart.png")
    plt.close()

    # === Barras: Nodos más visitados por tipo ===
    visit_counts = {"📦": {}, "🔋": {}, "👤": {}}
    for v in graph.vertices():
        name = str(v)
        for symbol in visit_counts:
            if name.startswith(symbol):
                visit_counts[symbol][name] = 0

    for order in sim.get_orders():
        for node in order.get("path", []):
            node_str = str(node)
            for symbol in visit_counts:
                if node_str in visit_counts[symbol]:
                    visit_counts[symbol][node_str] += 1

    tipos_info = {
        "👤": ("temp/top_visited_clients.png", "Top Visited Clients"),
        "🔋": ("temp/top_visited_recharges.png", "Top Visited Recharge Stations"),
        "📦": ("temp/top_visited_storages.png", "Top Visited Storage Nodes")
    }

    for tipo, (filename, title) in tipos_info.items():
        sorted_visits = sorted(visit_counts[tipo].items(), key=lambda x: x[1], reverse=True)[:5]
        if sorted_visits:
            nodos = [n[0] for n in sorted_visits]
            visitas = [n[1] for n in sorted_visits]

            fig, ax = plt.subplots()
            ax.bar(nodos, visitas, color="steelblue")
            ax.set_title(title)
            ax.set_xlabel("Nodo")
            ax.set_ylabel("Visitas")
            plt.savefig(filename)
            plt.close()




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

      # Sección: Gráficos
    img_height = 300
    img_width = 400
    margin = 50

    for img_path in [
        "temp/nodos_pie_chart.png",
        "temp/top_visited_clients.png",
        "temp/top_visited_recharges.png",
        "temp/top_visited_storages.png",
    ]:
        if os.path.exists(img_path):
            if y < img_height + margin:
                c.showPage()
                y = height - margin
            c.drawImage(img_path, 50, y - img_height, width=img_width, height=img_height)
            y -= img_height + 20  # deja un pequeño espacio entre gráficos

    
    # Finalizar PDF
    c.save()
    return ruta_salida
