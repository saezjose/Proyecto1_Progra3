# Para Inciarl Streamlit usa python -m streamlit hello

# sim/init_simulation.py

import random
from model.graph import Graph
from model.vertex import Vertex
from model.edge import Edge
from model.node_data import NodeData

def generar_red(n_nodes, m_edges, n_almacen, n_recarga, n_clientes):
    graph = Graph(directed=True)

    # Crear roles con metadata explícita (dict)
    roles = (
        [{"role": "almacen", "emoji": "📦", "id": f"N{i}"} for i in range(n_almacen)] +
        [{"role": "recarga", "emoji": "🔋", "id": f"N{i}"} for i in range(n_recarga)] +
        [{"role": "cliente", "emoji": "👤", "id": f"N{i}"} for i in range(n_clientes)]
    )

    random.shuffle(roles)

    vertices = []
    for i in range(n_nodes):
        data = roles[i]
        label = f"{data['emoji']} {data['id']}"
        vdata = NodeData(label, data["role"], data["id"])
        v = graph.insert_vertex(vdata)
        vertices.append(v)

    # Paso 1: Conectar todos los nodos en una cadena para asegurar conexidad
    for i in range(n_nodes - 1):
        u = vertices[i]
        v = vertices[i + 1]
        graph.insert_edge(u, v, random.randint(1, 10))

    # Paso 2: Agregar aristas aleatorias adicionales sin duplicar
    added = set((vertices[i], vertices[i + 1]) for i in range(n_nodes - 1))
    while len(added) < m_edges:
        u, v = random.sample(vertices, 2)
        if (u, v) not in added:
            graph.insert_edge(u, v, random.randint(1, 10))
            added.add((u, v))

    # Guardar los vértices para uso en selectbox (opcional)
    graph._vertices_list = vertices

    from sim.simulation import Simulation
    sim = Simulation(graph)
    return graph, sim
