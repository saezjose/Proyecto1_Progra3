from fastapi import APIRouter
from sim.init_simulation import generar_red

router = APIRouter()

graph, sim = generar_red(15, 20, 3, 3, 9)

@router.get("/")
def get_orders():
    return sim.get_orders()

@router.get("/orders/{order_id}")
def get_order(order_id: str):
    return sim.get_order_by_id(order_id)

@router.post("/orders/{order_id}/cancel")
def cancel_order(order_id: str):
    return sim.cancel_order(order_id)

@router.post("/orders/{order_id}/complete")
def complete_order(order_id: str):
    return sim.complete_order(order_id)
