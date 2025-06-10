# domain/client.py

class Client:
    def __init__(self, client_id, name, client_type="premium"):
        self.client_id = client_id
        self.name = name
        self.client_type = client_type
        self.orders = []

    def add_order(self, order_id):
        self.orders.append(order_id)

    def total_orders(self):
        return len(self.orders)

    def to_dict(self):
        return {
            "id": self.client_id,
            "name": self.name,
            "type": self.client_type,
            "total_orders": self.total_orders()
        }

    def __str__(self):
        return f"Cliente({self.client_id} - {self.name})"

    def __repr__(self):
        return str(self)
