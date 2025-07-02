from fastapi import FastAPI
from api.controllers import client_routes, order_routes, report_routes, info_routes

app = FastAPI(title="Sistema de Drones - API")

@app.get("/")
def root():
    return {"status": "API funcionando 🚀"}

# Incluir cada router en su respectivo prefijo
app.include_router(client_routes.router, prefix="/clients", tags=["Clientes"])
app.include_router(order_routes.router, prefix="/orders", tags=["Órdenes"])
app.include_router(report_routes.router, prefix="/reports", tags=["PDF Reports"])
app.include_router(info_routes.router, prefix="/routes", tags=["Rutas"])
