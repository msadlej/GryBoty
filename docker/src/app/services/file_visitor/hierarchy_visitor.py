import ast


class ClassHierarchyVisitor(ast.NodeVisitor):
    """
    A visitor class for analyzing class hierarchies in Python source code.

    This class constructs a tree representation of the inheritance hierarchy
    starting from a specified target base class. It assumes that a class does not
    inherit from multiple target base classes simultaneously.

    Attributes:
        tree (Tree): A tree structure representing the inheritance hierarchy,
                     initialized with the target base class as the root.

    Methods:
        generic_visit(node):
            Visits each node in the abstract syntax tree (AST) to identify class
            definitions and their parent-child relationships. Adds child classes
            to the tree if their parent matches the target base class or its descendants.
    """

    def __init__(self, target_base: str):
        self.tree = Tree(Node(target_base))

    def generic_visit(self, node):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            parents = [base.id for base in node.bases if isinstance(base, ast.Name)]
            class_node = Node(class_name)
            for parent in parents:
                parent_node = self.tree.find(parent)
                if parent_node is not None:
                    parent_node.children.append(class_node)
        super().generic_visit(node)


class Node:
    def __init__(self, data):
        self.data = data
        self.children = []


class Tree:
    def __init__(self, root):
        self.root = root

    def insert(self, parent: Node, child: Node):
        parent.children.append(child)

    def find(self, data_to_find: str):
        return self._find(self.root, data_to_find)  # Start from the root

    def _find(self, node: Node, data_to_find: str):
        if node.data == data_to_find:
            return node
        for child in node.children:
            result = self._find(child, data_to_find)
            if result:
                return result
        return None  # If not found

    def get_leaves(self):
        leaves = set()
        self._collect_leaves(self.root, leaves)
        return [node.data for node in leaves if node.data != self.root.data]

    def _collect_leaves(self, node: Node, leaves: list):
        if not node.children:  # No children = leaf
            leaves.add(node)
        for child in node.children:
            self._collect_leaves(child, leaves)
