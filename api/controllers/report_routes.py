from fastapi import APIRouter
from fastapi.responses import FileResponse
from sim.init_simulation import generar_red
from visual.report_generator import generar_pdf, guardar_graficos_pdf

router = APIRouter()

graph, sim = generar_red(15, 20, 3, 3, 9)

@router.get("/reports/pdf", response_class=FileResponse)
def descargar_pdf():
    orders = sim.get_orders()
    clients = sim.get_clients()
    rutas = sim.get_frequent_routes()

    guardar_graficos_pdf(graph, sim)
    path = generar_pdf(orders, clients, rutas)
    return FileResponse(path, filename="informe_drones.pdf", media_type="application/pdf")
