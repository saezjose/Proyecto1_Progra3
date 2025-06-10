# Para Inciarl Streamlit usa python -m streamlit run visual/dashboard.py

#HAY UNOS WARNINGS DE MATPLOTLIB ES QUE CUANODO SE GENERAN LOS NODOS SE CREAN CON UNOS EMOJIS QUE NO SON CAPACES DE PROCESAR HAY
#QUE QUITARLOS ESO Xd

import streamlit as st
from visual.networkx_adapter import NetworkXAdapter
from sim.init_simulation import generar_red
from sim.simulation import Simulation
from visual.avl_visualizer import AVLVisualizer


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
        st.success("Simulación iniciada correctamente 🚀")

# =============================
# 🌍 PESTAÑA 2: Explore Network
# =============================

with tabs[1]:
    st.header("🌍 Explora la Red de Drones")

    if st.session_state.get("simulation_started"):
        graph = st.session_state["graph"]
        sim = st.session_state["sim"]

        st.subheader("🔎 Visualización del grafo")
        adapter = NetworkXAdapter(graph)
        adapter.draw(st_target=st)

        st.subheader("✈ Calcular Ruta")
        vertices = list(graph.vertices())
        origin = st.selectbox("Nodo Origen", vertices, format_func=str)
        destination = st.selectbox("Nodo Destino", vertices, format_func=str)

        if st.button("✈ Calculate Route"):
            from collections import deque

            def bfs_con_bateria(grafo, origen, destino, bateria_max=50):
                visited = set()
                queue = deque()
                queue.append((origen, [origen], 0))

                while queue:
                    actual, path, cost = queue.popleft()

                    if actual == destino and cost <= bateria_max:
                        return path, cost

                    for vecino in grafo.neighbors(actual):
                        if vecino not in path:
                            edge = grafo.get_edge(actual, vecino)
                            nuevo_costo = cost + edge.element()

                            if nuevo_costo <= bateria_max:
                                queue.append((vecino, path + [vecino], nuevo_costo))

                return None, None

            path, cost = bfs_con_bateria(graph, origin, destination)

            if path:
                st.success(f"Ruta encontrada: {' → '.join(str(v) for v in path)} | Costo: {cost}")
                adapter.draw(st_target=st, highlight_path=path)

                if st.button("✅ Complete Delivery and Create Order"):
                    client_id = "client_test"
                    sim.register_client(client_id, "Cliente Test")
                    sim.create_order(client_id, origin, destination, 1, path, cost)
                    st.success("Orden creada y ruta registrada en AVL ✅")
            else:
                st.error("No hay ruta posible dentro del límite de batería (50).")
    else:
        st.info("Inicia una simulación en la pestaña anterior para usar esta sección.")

# ===============================
# 🌐 PESTAÑA 3: Clients & Orders
# ===============================

with tabs[2]:
    st.header("🌐 Clientes y Órdenes")

    if st.session_state.get("simulation_started"):
        sim = st.session_state["sim"]
        st.subheader("👤 Clientes")
        for c in sim.get_clients():
            st.json(c)

        st.subheader("📦 Órdenes")
        for o in sim.get_orders():
            st.json(o)
    else:
        st.info("Inicia una simulación para ver clientes y órdenes.")

# =============================
# 📋 PESTAÑA 4: Route Analytics
# =============================

with tabs[3]:
    st.header("📋 Route Frequency & History")

    if st.session_state.get("simulation_started"):
        sim = st.session_state["sim"]
        rutas = sim.get_frequent_routes()

        st.subheader("🔁 Rutas más frecuentes")
        for ruta, freq in rutas:
            st.markdown(f"- **{ruta}** | Frecuencia: {freq}")

        st.subheader("🌳 Visualización del árbol AVL")
        visualizer = AVLVisualizer(sim.routes_avl)
        visualizer.draw()
    else:
        st.info("Inicia una simulación para ver rutas frecuentes.")

# ==============================
# 📈 PESTAÑA 5: General Statistics
# ==============================

with tabs[4]:
    st.header("📈 Estadísticas Generales")

    st.info("(En construcción: Gráficas de nodos visitados y distribución de roles)")