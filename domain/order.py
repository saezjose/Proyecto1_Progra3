# domain/order.py
from datetime import datetime

class Order:
    def __init__(self, order_id, client_id, origin, destination, priority=1, path=None):
        self.order_id = order_id
        self.client_id = client_id
        self.origin = origin
        self.destination = destination
        self.priority = priority
        self.created_at = datetime.now()
        self.delivered_at = None
        self.status = "pending"
        self.total_cost = 0
        self.path = path or []

    def complete_delivery(self, cost):
        self.status = "delivered"
        self.delivered_at = datetime.now()
        self.total_cost = cost

    def to_dict(self):
        return {
            "id": self.order_id,
            "client_id": self.client_id,
            "origin": str(self.origin),
            "destination": str(self.destination),
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "delivered_at": self.delivered_at.strftime("%Y-%m-%d %H:%M:%S") if self.delivered_at else None,
            "total_cost": self.total_cost,
            "path": [str(p) for p in self.path]  # ✅ Agregado

            
        }

    def __str__(self):
        return f"Orden({self.order_id}) para cliente {self.client_id}"

    def __repr__(self):
        return str(self)
