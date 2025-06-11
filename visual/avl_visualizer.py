import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

class AVLVisualizer:
    def __init__(self, tree):
        self.tree = tree
        self.graph = nx.DiGraph()

    def _add_edges(self, node):
        if node:
            label = " → ".join(node.key) + f"\nFreq: {node.value}"
            self.graph.add_node(label)
            if node.left:
                left_label = " → ".join(node.left.key) + f"\nFreq: {node.left.value}"
                self.graph.add_edge(label, left_label)
                self._add_edges(node.left)
            if node.right:
                right_label = " → ".join(node.right.key) + f"\nFreq: {node.right.value}"
                self.graph.add_edge(label, right_label)
                self._add_edges(node.right)

    def draw(self, use_hierarchy=False):
        self.graph.clear()
        self._add_edges(self.tree.root)

        def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
            pos = {}
            def _hierarchy_pos(G, root, left, right, vert_loc, xcenter, pos):
                pos[root] = (xcenter, vert_loc)
                neighbors = list(G.neighbors(root))
                if neighbors:
                    dx = (right - left) / len(neighbors)
                    nextx = left + dx / 2
                    for neighbor in neighbors:
                        pos = _hierarchy_pos(G, neighbor, nextx - dx / 2, nextx + dx / 2, vert_loc - vert_gap, nextx, pos)
                        nextx += dx
                return pos
            return _hierarchy_pos(G, root, 0, width, vert_loc, xcenter, pos)

        pos = hierarchy_pos(self.graph, root=list(self.graph.nodes)[0]) if use_hierarchy else nx.spring_layout(self.graph)

        plt.figure(figsize=(10, 6))
        nx.draw(self.graph, pos, with_labels=True, node_color='#87CEFA', node_size=2500, font_size=10, font_weight='bold', arrows=True)
        plt.title("AVL Tree Visualization")
        plt.tight_layout()
        st.pyplot(plt)
