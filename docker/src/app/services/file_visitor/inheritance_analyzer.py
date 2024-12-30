import ast
from src.app.services.file_visitor.hierarchy_visitor import ClassHierarchyVisitor


class InheritanceAnalyzer:
    def __init__(self, source_code, target_bases):
        self.tree = ast.parse(source_code)
        self.visitor = ClassHierarchyVisitor(target_bases)
        self.visitor_result = self.visitor.visit(self.tree)

    """
    A utility class for analyzing inheritance hierarchies in Python source code.

    This class provides a static method to determine the leaf nodes (i.e.,
    the most derived classes) of an inheritance hierarchy that originates
    from a specified base class.

    Methods:
        get_last_children(source_code, target_bases):
            Parses the given source code to identify the inheritance hierarchy
            for the specified target base class and returns a list of the leaf
            nodes in the hierarchy.

    Usage:
        source_code = '''
        class A: pass
        class B(A): pass
        class C(B): pass
        '''
        result = InheritanceAnalyzer.get_last_children(source_code, "A")
        print(result)  # Output: ["C"]
    """

    def get_last_children(self):
        return self.visitor.tree.get_leaves()
