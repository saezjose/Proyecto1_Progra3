from fastapi import APIRouter
from fastapi.responses import FileResponse
from visual.report_generator import generar_pdf
from sim.init_simulation import generar_red

router = APIRouter()

@router.get("/pdf", response_class=FileResponse)
def descargar_informe_pdf():
    graph, sim = generar_red(15, 20, 3, 3, 9)
    orders = sim.get_orders()
    clients = sim.get_clients()
    rutas = sim.get_frequent_routes()

    path = generar_pdf(orders, clients, rutas)
    return FileResponse(path, filename="informe_drones.pdf", media_type="application/pdf")
