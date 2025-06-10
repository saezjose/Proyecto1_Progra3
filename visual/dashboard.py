# Para Inciarl Streamlit usa python -m streamlit run visual/dashboard.py

#HAY UNOS WARNINGS DE MATPLOTLIB ES QUE CUANODO SE GENERAN LOS NODOS SE CREAN CON UNOS EMOJIS QUE NO SON CAPACES DE PROCESAR HAY
#QUE QUITARLOS ESO Xd

import streamlit as st
from visual.networkx_adapter import NetworkXAdapter
from sim.init_simulation import generar_red
from sim.simulation import Simulation
from visual.avl_visualizer import AVLVisualizer
import random
import pandas as pd
from collections import deque



# Configuración de la interfaz
st.set_page_config(page_title="Sistema de Drones", layout="wide")

# Sidebar de navegación (5 pestañas)
tabs = st.tabs(["🔄 Run Simulation", "🌍 Explore Network", "🌐 Clients & Orders", "📋 Route Analytics", "📈 General Statistics"])

# ============================
# 🔄 PESTAÑA 1: Run Simulation
# ============================

with tabs[0]:
    st.header("🔄 Simulación de Red de Drones")

    st.markdown("Configura los parámetros para iniciar la simulación:")

    n_nodes = st.slider("Número de nodos", min_value=10, max_value=150, value=15)
    m_edges = st.slider("Número de aristas", min_value=n_nodes - 1, max_value=min(300, n_nodes*(n_nodes - 1)//2), value=20)
    n_orders = st.slider("Número de órdenes", min_value=10, max_value=300, value=10)

    n_almacen = int(n_nodes * 0.20)
    n_recarga = int(n_nodes * 0.20)
    n_clientes = n_nodes - n_almacen - n_recarga

    st.markdown("""
    **Distribución de nodos:**  
    📦 Almacenamiento: {} (20%)  
    🔋 Recarga: {} (20%)  
    👤 Clientes: {} (60%)
    """.format(n_almacen, n_recarga, n_clientes))

    if st.button("📊 Start Simulation"):
        graph = generar_red(n_nodes, m_edges, n_almacen, n_recarga, n_clientes)
        sim = Simulation(graph)

        # Registrar clientes automáticamente
        for i in range(n_clientes):
            client_id = f"C{i:03}"
            name = f"Cliente {i}"
            client_type = random.choice(["premium", "normal"])
            sim.register_client(client_id, name, client_type)

        # Función para encontrar rutas válidas con BFS
        def bfs(graph, start, end):
            visited = set()
            queue = deque([(start, [start], 0)])

            while queue:
                current, path, cost = queue.popleft()
                if current == end:
                    return path, cost
                for neighbor in graph.neighbors(current):
                    if neighbor not in path:
                        edge = graph.get_edge(current, neighbor)
                        queue.append((neighbor, path + [neighbor], cost + edge.element()))
            return None, None

        vertices = list(graph.vertices())
        client_nodes = [v for v in vertices if "Cliente" in str(v)]
        if len(client_nodes) >= 2:
            for i in range(min(n_orders, len(client_nodes))):
                origin = random.choice(client_nodes)
                destination = random.choice([v for v in client_nodes if v != origin])
                path, cost = bfs(graph, origin, destination)
                if path:
                    sim.create_order(f"C{i:03}", origin, destination, priority=1, path=path, cost=cost)

        st.session_state["graph"] = graph
        st.session_state["sim"] = sim
        st.session_state["simulation_started"] = True
        st.session_state["adapter"] = NetworkXAdapter(graph)

        st.success("Simulación iniciada correctamente 🚀")


# =============================
# 🌍 PESTAÑA 2: Explore Network
# =============================

with tabs[1]:
    st.header("🌍 Explora la Red de Drones")

    if st.session_state.get("simulation_started"):
        graph = st.session_state["graph"]
        adapter = st.session_state["adapter"]

        st.subheader("🚁 Visualización del grafo")

        st.subheader("🧱 Calcular Ruta")
        vertices = getattr(graph, "_vertices_list", list(graph.vertices()))

        origin = st.selectbox("Nodo de Origen", vertices, format_func=str)
        destination = st.selectbox("Nodo de Destino", vertices, format_func=str)

        if st.button("✈ Calculate Route"):
            from collections import deque

            def bfs_shortest_path(graph, start, goal):
                visited = set()
                queue = deque([(start, [start])])

                while queue:
                    current, path = queue.popleft()
                    if current == goal:
                        return path
                    for neighbor in graph.neighbors(current):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append((neighbor, path + [neighbor]))
                return None

            path = bfs_shortest_path(graph, origin, destination)

            if path:
                st.success("Ruta encontrada:")
                st.markdown(" → ".join(str(v) for v in path))
                adapter.draw(st_target=st, highlight_path=path)
            else:
                st.error("No se encontró una ruta entre los nodos seleccionados.")
        else:
            adapter.draw(st_target=st)
    else:
        st.info("Inicia una simulación en la pestaña anterior para usar esta sección.")

        

# ==========================
# 🌐 PESTAÑA 3: Clients & Orders
# ==========================

with tabs[2]:
    st.header("🌐 Clients and Orders")

    if st.session_state.get("simulation_started"):
        sim = st.session_state["sim"]

        st.subheader("👤 Clients")
        clients = sim.get_clients()
        if clients:
            for client in clients:
                if "type" not in client:
                    client["type"] = random.choice(["premium", "normal"])
            st.dataframe(pd.DataFrame(clients))
        else:
            st.info("No hay clientes registrados todavía.")

        st.subheader("📦 Orders")
        orders = sim.get_orders()
        if orders:
            st.dataframe(pd.DataFrame(orders))
        else:
            st.info("No hay órdenes registradas todavía.")
    else:
        st.info("Inicia una simulación para ver clientes y órdenes.")

 # =============================
# 📋 PESTAÑA 4: Route Analytics
# =============================

with tabs[3]:
    st.header("📋 Route Analytics")

    if st.session_state.get("simulation_started"):
        sim = st.session_state["sim"]
        rutas = sim.get_frequent_routes()

        if rutas:
            rutas.sort()  # Ordenar por recorrido (orden lexicográfico)

            st.subheader("🔁 Rutas más frecuentes")
            for ruta, freq in rutas:
                st.markdown(f"- **{ruta}** | Frecuencia: {freq}")

            st.subheader("🌳 Visualización del árbol AVL")
            from visual.avl_visualizer import AVLVisualizer
            visualizer = AVLVisualizer(sim.routes_avl)
            visualizer.draw()
        else:
            st.warning("No hay rutas registradas aún.")
    else:
        st.info("Inicia una simulación para analizar rutas.")

# ==============================
# 📈 PESTAÑA 5: General Statistics
# ==============================
with tabs[4]:
    st.header("📈 General Statistics")

import matplotlib.pyplot as plt
import math

# Asegurar que se guarde el grafo si no existe
if "graph" not in st.session_state and st.session_state.get("params"):
    from sim.init_simulation import generar_red
    params = st.session_state["params"]
    st.session_state["graph"] = generar_red(
        params["n_nodes"],
        params["m_edges"],
        params["n_almacen"],
        params["n_recarga"],
        params["n_clientes"]
    )

graph = st.session_state.get("graph")
if graph:
    roles = {"📦": "Almacenamiento", "🔋": "Recarga", "👤": "Cliente"}
    role_counts = {"📦": 0, "🔋": 0, "👤": 0}

    for v in graph.vertices():
        for symbol in roles:
            if str(v).startswith(symbol):
                role_counts[symbol] += 1

    labels = [roles[k] for k in role_counts]
    sizes = [int(role_counts[k]) if role_counts[k] and not math.isnan(role_counts[k]) else 0 for k in role_counts]

    if sum(sizes) > 0:
        # Gráfico de torta - proporción de roles
        st.subheader("🥧 Distribución de Nodos por Rol")
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax1.axis("equal")
        st.pyplot(fig1)

        # Gráfico de barras - cantidad por rol
        st.subheader("📊 Cantidad de Nodos por Rol")
        fig2, ax2 = plt.subplots()
        ax2.bar(labels, sizes, color=["#ffd166", "#118ab2", "#ef476f"])
        ax2.set_ylabel("Cantidad")
        ax2.set_title("Cantidad de nodos por tipo")
        st.pyplot(fig2)
    else:
        st.warning("No hay nodos registrados para mostrar estadísticas.")
else:
    st.warning("No se encontró un grafo generado.")
