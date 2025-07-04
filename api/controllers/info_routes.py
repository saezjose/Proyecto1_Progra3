from fastapi import APIRouter
from sim.init_simulation import generar_red

router = APIRouter()

graph, sim = generar_red(15, 20, 3, 3, 9)

@router.get("/reports/visits/clients")
def get_most_visited_clients():
    return sim.get_most_visited_clients()

@router.get("/reports/visits/recharges")
def get_most_visited_recharges():
    return sim.get_most_visited_recharges()

@router.get("/reports/visits/storages")
def get_most_visited_storages():
    return sim.get_most_visited_storages()

@router.get("/reports/summary")
def get_summary():
    return sim.get_simulation_summary()
