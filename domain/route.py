# domain/route.py

class Route:
    def __init__(self, path, cost):
        """
        path: lista de nodos recorridos (por ejemplo: [V1, V2, V3])
        cost: costo total de la ruta (suma de pesos de aristas)
        """
        self.path = path
        self.cost = cost

    def to_str_path(self):
        """Devuelve la ruta como string: A → B → C"""
        return " → ".join(str(v) for v in self.path)

    def to_key(self):
        """Clave para usar en AVL: misma ruta = misma clave"""
        return tuple(str(v) for v in self.path)

    def to_dict(self):
        return {
            "path": self.to_str_path(),
            "cost": self.cost
        }

    def __str__(self):
        return f"Ruta({self.to_str_path()} | Costo: {self.cost})"

    def __repr__(self):
        return str(self)
