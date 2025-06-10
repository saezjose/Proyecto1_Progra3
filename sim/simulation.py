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

        order = Order(order_id, client_id, origin, destination, priority)
        order.complete_delivery(cost)
        self.orders.set(order_id, order)

        client = self.clients.get(client_id)
        if client:
            client.add_order(order_id)

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
