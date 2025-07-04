from fastapi import APIRouter
from sim.init_simulation import generar_red

router = APIRouter()

graph, sim = generar_red(15, 20, 3, 3, 9)

@router.get("/")
def get_clients():
    return sim.get_clients()

@router.get("/{client_id}")
def get_client(client_id: str):
    return sim.get_client_by_id(client_id)
