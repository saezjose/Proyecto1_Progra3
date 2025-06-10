# Para Inciarl Streamlit usa python -m streamlit run visual/dashboard.py

#HAY UNOS WARNINGS DE MATPLOTLIB ES QUE CUANODO SE GENERAN LOS NODOS SE CREAN CON UNOS EMOJIS QUE NO SON CAPACES DE PROCESAR HAY
#QUE QUITARLOS ESO Xd

import streamlit as st
from visual.networkx_adapter import NetworkXAdapter
from sim.init_simulation import generar_red
from sim.simulation import Simulation
from visual.avl_visualizer import AVLVisualizer
import random


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
        for client in clients:
            client_type = client.get("type")
            if not client_type:
                # Asignar aleatoriamente tipo si no existe
                client_type = random.choice(["premium", "normal"])
            st.json({
                "client_id": client["id"],
                "name": client["name"],
                "type": client_type,
                "total_orders": client["total_orders"]
            })

        st.subheader("📦 Orders")
        orders = sim.get_orders()
        for order in orders:
            st.json({
                "order_id": order["id"],
                "client": order.get("client", order["client_id"]),
                "client_id": order["client_id"],
                "origin": str(order["origin"]),
                "destination": str(order["destination"]),
                "status": order["status"],
                "priority": order["priority"],
                "created_at": order["created_at"],
                "delivered_at": order.get("delivered_at", None),
                "route_cost": order.get("total_cost", 0)
            })
    else:
        st.info("Inicia una simulación para ver clientes y órdenes.")
