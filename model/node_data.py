# model/node_data.py

class NodeData:
    def __init__(self, label, role, id):
        self.label = label
        self.role = role
        self.id = id

    def __hash__(self):
        return hash((self.label, self.role, self.id))

    def __eq__(self, other):
        return isinstance(other, NodeData) and \
               self.label == other.label and \
               self.role == other.role and \
               self.id == other.id

    def __str__(self):
        return self.label

    def __repr__(self):
        return f"NodeData({self.label}, {self.role}, {self.id})"
