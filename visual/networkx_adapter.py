# visual/networkx_adapter.py

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from typing import Dict, List, Optional, Sequence, Tuple

try:
    import streamlit as st  # type: ignore
except ModuleNotFoundError:
    st = None  # type: ignore

class NetworkXAdapter:
    ROLE_COLORS: Dict[str, str] = {
        "almacen": "#ffd166",
        "recarga": "#118ab2",
        "cliente": "#ef476f",
    }
    DEFAULT_COLOR = "#8d99ae"

    def __init__(self, custom_graph, *, seed: int = 13):
        self._custom_graph = custom_graph
        self._seed = seed
        self._nx_graph: nx.Graph = (
            nx.DiGraph() if custom_graph.is_directed() else nx.Graph()
        )
        self._vertex_labels: Dict[object, str] = {}
        self._build_graph()

    def _vertex_label(self, v) -> str:
        element = v.element()
        return getattr(element, "label", str(element))

    def _node_role(self, v) -> Optional[str]:
        element = v.element()
        return getattr(element, "role", None)

    def _build_graph(self):
        for v in self._custom_graph.vertices():
            label = self._vertex_label(v)
            role = self._node_role(v)
            self._vertex_labels[v] = label
            self._nx_graph.add_node(v, label=label, role=role)

        for e in self._custom_graph.edges():
            u, w = e.endpoints()
            weight = e.element()
            self._nx_graph.add_edge(u, w, weight=weight)

    def update(self):
        self._nx_graph.clear()
        self._build_graph()

    def positions(self) -> Dict[object, Tuple[float, float]]:
        return nx.spring_layout(self._nx_graph, seed=self._seed)

    def draw(
        self,
        *,
        highlight_path: Optional[Sequence] = None,
        show_weights: bool = True,
        figsize: Tuple[int, int] = (10, 6),
        st_target=None,
    ) -> None:
        pos = self.positions()

        node_colors = []
        for v in self._nx_graph.nodes():
            role = self._nx_graph.nodes[v].get("role")
            node_colors.append(self.ROLE_COLORS.get(role, self.DEFAULT_COLOR))

        edge_colors = []
        highlight_set = set()
        if highlight_path and len(highlight_path) > 1:
            pairs = zip(highlight_path, highlight_path[1:])
            highlight_set = set(pairs)
            highlight_set |= {(v, u) for u, v in highlight_set}

        for u, v in self._nx_graph.edges():
            edge_colors.append("#d90429" if (u, v) in highlight_set else "#2b2d42")

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

        # Agregar leyenda
        legend_patches = [
            mpatches.Patch(color=color, label=role.capitalize())
            for role, color in self.ROLE_COLORS.items()
        ]
        plt.legend(handles=legend_patches, loc="lower left")

        plt.axis("off")

        if st_target is not None:
            st_target.pyplot(plt)
            plt.close()
        elif st is not None:
            st.pyplot(plt)  # type: ignore
            plt.close()
        else:
            plt.show()

    @property
    def nx_graph(self) -> nx.Graph:
        return self._nx_graph

    def shortest_path(self, source, target) -> List:
        return nx.dijkstra_path(self._nx_graph, source=source, target=target, weight="weight")
