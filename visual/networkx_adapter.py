# visual/networkx_adapter.py
"""
Adaptador entre tu estructura de grafo propia (Graph, Vertex, Edge) y networkx,
con utilidades para dibujar y resaltar rutas desde Streamlit.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
from typing import Dict, List, Optional, Sequence, Tuple

# Streamlit es opcional: el módulo solo se usa si se ejecuta dentro de Streamlit
try:
    import streamlit as st  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    st = None  # type: ignore


class NetworkXAdapter:
    """Convierte un ``Graph`` propio en un ``networkx.Graph`` para visualización.

    Parámetros
    ----------
    custom_graph : Graph
        Instancia de tu TDA ``Graph``.
    seed : int, opcional
        Semilla para el layout de posiciones (spring_layout).
    """

    # Paleta pastel consistente con los iconos usados en el dashboard
    ROLE_COLORS: Dict[str, str] = {
        "almacen": "#ffd166",   # 📦
        "recarga": "#118ab2",   # 🔋
        "cliente": "#ef476f",   # 👤
    }
    DEFAULT_COLOR = "#8d99ae"

    def __init__(self, custom_graph, *, seed: int = 13):
        self._custom_graph = custom_graph
        self._seed = seed
        # DiGraph si el grafo es dirigido, en caso contrario Graph
        self._nx_graph: nx.Graph = (
            nx.DiGraph() if custom_graph.is_directed() else nx.Graph()
        )
        # Etiquetas para los vértices {Vertex -> str}
        self._vertex_labels: Dict[object, str] = {}
        self._build_graph()

    # ------------------------------------------------------------------
    # Construcción y sincronización
    # ------------------------------------------------------------------
    def _vertex_label(self, v) -> str:
        """Devuelve una etiqueta corta para mostrar en pantalla."""
        element = v.element()
        if isinstance(element, dict):
            # Permitimos que el alumno guarde id/role en un dict
            return str(element.get("id", element))
        return str(element)

    def _node_role(self, v) -> Optional[str]:
        element = v.element()
        if isinstance(element, dict):
            return element.get("role")
        return None

    def _build_graph(self):
        """Vuelca todos los vértices y aristas al objeto networkx."""
        # --- Nodos ---
        for v in self._custom_graph.vertices():
            label = self._vertex_label(v)
            role = self._node_role(v)
            self._vertex_labels[v] = label
            self._nx_graph.add_node(v, label=label, role=role)

        # --- Aristas ---
        for e in self._custom_graph.edges():
            u, w = e.endpoints()
            weight = e.element()
            self._nx_graph.add_edge(u, w, weight=weight)

    def update(self):
        """Reconstruye el grafo. Llamar tras insertar/eliminar nodos o aristas."""
        self._nx_graph.clear()
        self._build_graph()

    # ------------------------------------------------------------------
    # Posiciones y helpers
    # ------------------------------------------------------------------
    def positions(self) -> Dict[object, Tuple[float, float]]:
        """Posiciones (dict) para nx.draw usando spring_layout con semilla fija."""
        return nx.spring_layout(self._nx_graph, seed=self._seed)

    # ------------------------------------------------------------------
    # Dibujo
    # ------------------------------------------------------------------
    def draw(
        self,
        *,
        highlight_path: Optional[Sequence] = None,
        show_weights: bool = False,
        figsize: Tuple[int, int] = (10, 6),
        st_target=None,
    ) -> None:
        """Dibuja el grafo; si ``highlight_path`` se pasa, resalta esa ruta en rojo.

        Parameters
        ----------
        highlight_path : Sequence, opcional
            Secuencia de vértices (u, v, w, ...) que forman la ruta a resaltar.
        show_weights : bool, opcional
            Muestra etiquetas de peso de las aristas.
        figsize : tuple, opcional
            Tamaño de la figura en pulgadas.
        st_target : module, opcional
            Normalmente el módulo ``streamlit`` (``st``) para que el gráfico se
            incruste vía ``st.pyplot``; si se omite o es ``None``, usa ``plt.show``.
        """
        pos = self.positions()

        # --- Colores por nodo ---
        node_colors = []
        for v in self._nx_graph.nodes():
            role = self._nx_graph.nodes[v].get("role")
            node_colors.append(self.ROLE_COLORS.get(role, self.DEFAULT_COLOR))

        # --- Colores por arista ---
        edge_colors = []
        highlight_set = set()
        if highlight_path and len(highlight_path) > 1:
            pairs = zip(highlight_path, highlight_path[1:])
            highlight_set = set(pairs)
            # Para grafos no dirigidos, añadimos inversas
            highlight_set |= {(v, u) for u, v in highlight_set}

        for u, v in self._nx_graph.edges():
            edge_colors.append("#d90429" if (u, v) in highlight_set else "#2b2d42")

        # --- Dibujo ---
        plt.figure(figsize=figsize)
        nx.draw(
            self._nx_graph,
            pos,
            with_labels=True,
            labels={v: self._vertex_labels[v] for v in self._nx_graph.nodes()},
            node_color=node_colors,
            edge_color=edge_colors,
            node_size=900,
            font_size=9,
            width=2,
        )

        if show_weights:
            edge_labels = nx.get_edge_attributes(self._nx_graph, "weight")
            nx.draw_networkx_edge_labels(
                self._nx_graph, pos, edge_labels=edge_labels, font_size=8
            )

        plt.axis("off")
        plt.tight_layout()

        # --- Envío a Streamlit o pantalla ---
        if st_target is not None:
            st_target.pyplot(plt)
            plt.close()
        elif st is not None:
            st.pyplot(plt)  # type: ignore
            plt.close()
        else:
            plt.show()

    # ------------------------------------------------------------------
    # Accesos a networkx por si se requiere
    # ------------------------------------------------------------------
    @property
    def nx_graph(self) -> nx.Graph:
        """Devuelve el grafo de networkx (lectura)."""
        return self._nx_graph

    def shortest_path(self, source, target) -> List:
        """Camino más corto según peso de arista (Dijkstra)."""
        # Si no se han definido pesos, networkx asume peso 1.
        return nx.dijkstra_path(self._nx_graph, source=source, target=target, weight="weight")
