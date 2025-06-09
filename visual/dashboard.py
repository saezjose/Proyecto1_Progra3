# Para Inciarl Streamlit usa python -m streamlit run visual/dashboard.py


import streamlit as st

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

    # Sliders de configuración
    n_nodes = st.slider("Número de nodos", min_value=10, max_value=150, value=15)
    m_edges = st.slider("Número de aristas", min_value=n_nodes - 1, max_value=min(300, n_nodes*(n_nodes - 1)//2), value=20)
    n_orders = st.slider("Número de órdenes", min_value=10, max_value=300, value=10)

    # Cálculo de porcentaje de roles
    n_almacen = int(n_nodes * 0.20)
    n_recarga = int(n_nodes * 0.20)
    n_clientes = n_nodes - n_almacen - n_recarga

    st.info(f"Nodos de almacenamiento 📦: {n_almacen} | Estaciones de recarga 🔋: {n_recarga} | Clientes 👤: {n_clientes}")

    if st.button("📊 Start Simulation"):
        st.success("Simulación iniciada correctamente 🚀")
        st.session_state["simulation_started"] = True
        st.session_state["params"] = {
            "n_nodes": n_nodes,
            "m_edges": m_edges,
            "n_orders": n_orders,
            "n_almacen": n_almacen,
            "n_recarga": n_recarga,
            "n_clientes": n_clientes
        }
