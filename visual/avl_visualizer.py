import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

class AVLVisualizer:
    def __init__(self, avl_tree):
        self.tree = avl_tree
        self.graph = nx.DiGraph()

    def _add_edges(self, node):
        if node is None:
            return
        label = f"{node.key}\nFreq: {node.value}"
        self.graph.add_node(label)

        if node.left:
            left_label = f"{node.left.key}\nFreq: {node.left.value}"
            self.graph.add_edge(label, left_label)
            self._add_edges(node.left)

        if node.right:
            right_label = f"{node.right.key}\nFreq: {node.right.value}"
            self.graph.add_edge(label, right_label)
            self._add_edges(node.right)

    def draw(self):
        self.graph.clear()
        self._add_edges(self.tree.root)

        pos = nx.spring_layout(self.graph, seed=42)  # layout alternativo sin pygraphviz
        plt.figure(figsize=(12, 6))
        nx.draw(self.graph, pos, with_labels=True, node_size=2500, node_color="skyblue", font_size=10)
        plt.title("AVL Tree Visualization")
        plt.tight_layout()
        st.pyplot(plt)  # muestra dentro de Streamlit

