from fastapi import APIRouter
from sim.init_simulation import generar_red

router = APIRouter()

@router.get("/")
def listar_rutas_frecuentes():
    _, sim = generar_red(15, 20, 3, 3, 9)
    return sim.get_frequent_routes()
