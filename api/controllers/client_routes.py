from fastapi import APIRouter
from sim.init_simulation import generar_red

router = APIRouter()

@router.get("/")
def listar_clientes():
    _, sim = generar_red(15, 20, 3, 3, 9)
    return sim.get_clients()
