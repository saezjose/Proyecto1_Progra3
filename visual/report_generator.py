def generar_pdf(orders, clients, rutas):
    # Genera el PDF y retorna la ruta del archivo guardado
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    import os

    output_path = "temp/informe_drones.pdf"
    os.makedirs("temp", exist_ok=True)

    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 50, "📄 Informe de Entregas de Drones")
    c.drawString(100, height - 80, f"Total Órdenes: {len(orders)}")
    c.drawString(100, height - 100, f"Clientes Registrados: {len(clients)}")
    c.drawString(100, height - 120, f"Rutas Frecuentes: {len(rutas)}")

    c.save()
    return output_path
