# sim/simulation.py

from domain.order import Order
from domain.client import Client
from domain.route import Route
from tda.avl import AVLTree
from tda.hasp_map import HashMap
from model.graph import Graph

class Simulation:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.orders = HashMap()
        self.clients = HashMap()
        self.routes_avl = AVLTree()
        self.order_counter = 1

    def register_client(self, client_id, name, client_type="premium"):
        if not self.clients.contains(client_id):
            client = Client(client_id, name, client_type)
            self.clients.set(client_id, client)

    def create_order(self, client_id, origin, destination, priority, path, cost):
        order_id = f"ORD{self.order_counter}"
        self.order_counter += 1

        # Crear orden SIN marcarla como entregada aún
        order = Order(order_id, client_id, origin, destination, priority, path=path)
        order.total_cost = cost
        self.orders.set(order_id, order)

        client = self.clients.get(client_id)
        if client:
            client.add_order(order_id)

        # Registrar la ruta en el árbol AVL
        route = Route(path, cost)
        self.routes_avl.insert(route.to_key())

        return order

    def get_orders(self):
        return [o.to_dict() for _, o in self.orders.items()]

    def get_clients(self):
        return [c.to_dict() for _, c in self.clients.items()]

    def get_frequent_routes(self):
        result = []

        def _inorder(node):
            if not node:
                return
            _inorder(node.left)
            route_str = " → ".join(node.key)
            result.append((route_str, node.value))
            _inorder(node.right)

        _inorder(self.routes_avl.root)
        return result
    
    def get_simulation_summary(self):
        return {
            "total_clients": len(list(self.clients.keys())),
            "total_orders": len(list(self.orders.keys())),
            "completed_orders": len([o for _, o in self.orders.items() if o.status == "delivered"]),
            "pending_orders": len([o for _, o in self.orders.items() if o.status == "pending"]),
            "cancelled_orders": len([o for _, o in self.orders.items() if o.status == "cancelled"]),
        }

    def get_most_visited_clients(self):
        clients = [c for _, c in self.clients.items()]
        clients.sort(key=lambda c: len(c.orders), reverse=True)
        return [c.to_dict() for c in clients]

    def get_most_visited_recharges(self):
        counts = {}
        for _, order in self.orders.items():
            for node in order.path:
                if str(node).startswith("🔋"):
                    counts[str(node)] = counts.get(str(node), 0) + 1
        return sorted(counts.items(), key=lambda x: x[1], reverse=True)

    def get_most_visited_storages(self):
        counts = {}
        for _, order in self.orders.items():
            for node in order.path:
                if str(node).startswith("📦"):
                    counts[str(node)] = counts.get(str(node), 0) + 1
        return sorted(counts.items(), key=lambda x: x[1], reverse=True)

    def get_client_by_id(self, client_id):
        if self.clients.contains(client_id):
            return self.clients.get(client_id).to_dict()
        return None

    def get_order_by_id(self, order_id):
        if self.orders.contains(order_id):
            return self.orders.get(order_id).to_dict()
        return None

    def cancel_order(self, order_id):
        if self.orders.contains(order_id):
            order = self.orders.get(order_id)
            order.status = "cancelled"
            return {"status": "cancelled"}
        return {"error": "order not found"}

    def complete_order(self, order_id):
        if self.orders.contains(order_id):
            order = self.orders.get(order_id)
            order.status = "delivered"
            return {"status": "delivered"}
        return {"error": "order not found"}


