import folium
from folium import PolyLine
from typing import List, Tuple
import streamlit as st

def generar_mapa(nodos: List[Tuple[str, float, float, str]], aristas: List[Tuple[str, str, int]], ruta=None, mst=None):
    if not nodos:
        return None

    mapa = folium.Map(location=(nodos[0][1], nodos[0][2]), zoom_start=13)
    colores = {"📦": "blue", "🔋": "green", "👤": "red"}
    pos = {}

    # 🎯 1. Mostrar tipo de nodo con emoji como tooltip
    for nombre, lat, lon, tipo in nodos:
        color = colores.get(tipo[0], "gray")
        folium.CircleMarker(
            location=(lat, lon),
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            tooltip=f"{tipo} {nombre}"  # Se muestra al pasar el mouse
        ).add_to(mapa)
        pos[nombre] = (lat, lon)

    # Aristas normales (grises)
    for origen, destino, peso in aristas:
        if origen in pos and destino in pos:
            puntos = [pos[origen], pos[destino]]
            folium.PolyLine(puntos, color="gray", weight=2, tooltip=f"Peso: {peso}").add_to(mapa)

    # 🎯 2. Ruta calculada (roja) con costo total como tooltip
    if ruta and len(ruta) >= 2:
        puntos = [pos[n] for n in ruta if n in pos]
        costo_total = st.session_state.get("ruta_costo", "?")
        tooltip_text = f"Ruta calculada\nCosto total: {costo_total}"
        folium.PolyLine(puntos, color="red", weight=4, tooltip=tooltip_text).add_to(mapa)

    # MST (líneas naranjas discontinuas)
    if mst:
        for origen, destino, peso in mst:
            if origen in pos and destino in pos:
                puntos = [pos[origen], pos[destino]]
                folium.PolyLine(puntos, color="orange", weight=2, dash_array="5", tooltip=f"MST: {peso}").add_to(mapa)

    return mapa
