# domain/client.py

class Client:
    def __init__(self, client_id, name):
        self.client_id = client_id
        self.name = name
        self.orders = []  # Lista de IDs de órdenes

    def add_order(self, order_id):
        self.orders.append(order_id)

    def total_orders(self):
        return len(self.orders)

    def to_dict(self):
        return {
            "id": self.client_id,
            "name": self.name,
            "total_orders": self.total_orders()
        }

    def __str__(self):
        return f"Cliente({self.client_id} - {self.name})"

    def __repr__(self):
        return str(self)
