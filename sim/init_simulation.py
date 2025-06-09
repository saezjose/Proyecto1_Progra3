# Para Inciarl Streamlit usa python -m streamlit hello

# sim/init_simulation.py

import random
from model.graph import Graph
from model.vertex import Vertex
from model.edge import Edge


def generar_red(n_nodes, m_edges, n_almacen, n_recarga, n_clientes):
    graph = Graph(directed=True)

    # Asignar roles
    roles = ["ROL"] * n_almacen + ["Bateria"] * n_recarga + ["Cliente"] * n_clientes
    random.shuffle(roles)

    vertices = []
    for i in range(n_nodes):
        label = f"{roles[i]} N{i}"
        v = graph.insert_vertex(label)
        vertices.append(v)

    # Agregar aristas aleatorias
    added = set()
    while len(added) < m_edges:
        u, v = random.sample(vertices, 2)
        if (u, v) not in added:
            graph.insert_edge(u, v, random.randint(1, 10))
            added.add((u, v))

    return graph
