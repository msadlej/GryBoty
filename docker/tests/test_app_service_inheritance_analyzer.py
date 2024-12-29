import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))


class TestInheritanceAnalyzer(unittest.TestCase):

    def test_single_inheritance(self):
        from src.app.services.file_visitor.inheritance_analyzer import InheritanceAnalyzer

        source_code = """
class Animal:
    pass

class Mammal(Animal):
    pass

class Bird(Animal):
    pass

class Dog(Mammal):
    pass
"""
        target_bases = "Animal"
        result = InheritanceAnalyzer.get_last_children(source_code, target_bases)

        self.assertEqual(result, ["Dog", "Bird"])

    def test_multiple_inheritance(self):
        from src.app.services.file_visitor.inheritance_analyzer import InheritanceAnalyzer

        source_code = """
class Base1:
    pass

class Base2:
    pass

class Combined(Base1, Base2):
    pass
"""
        target_bases = "Base1"
        result = InheritanceAnalyzer.get_last_children(source_code, target_bases)

        self.assertEqual(result, ["Combined"])

    def test_deep_hierarchy(self):
        from src.app.services.file_visitor.inheritance_analyzer import InheritanceAnalyzer

        source_code = """
class Root:
    pass

class Level1(Root):
    pass

class Level2(Level1):
    pass

class Level3(Level2):
    pass
"""
        target_bases = "Root"
        result = InheritanceAnalyzer.get_last_children(source_code, target_bases)

        self.assertEqual(result, ["Level3"])

    def test_no_inheritance(self):
        from src.app.services.file_visitor.inheritance_analyzer import InheritanceAnalyzer

        source_code = """
class Independent:
    pass
"""
        target_bases = "Base"
        result = InheritanceAnalyzer.get_last_children(source_code, target_bases)

        self.assertEqual(result, [])

    def test_complex_hierarchy(self):
        from src.app.services.file_visitor.inheritance_analyzer import InheritanceAnalyzer

        source_code = """
class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass

class E(D):
    pass
"""
        target_bases = "A"
        result = InheritanceAnalyzer.get_last_children(source_code, target_bases)

        self.assertEqual(result, ["E"])

    def test_multiple_base_classes(self):
        from src.app.services.file_visitor.inheritance_analyzer import InheritanceAnalyzer

        source_code = """
class BaseA:
    pass

class BaseB:
    pass

class Derived(BaseA, BaseB):
    pass

class Final(Derived):
    pass
"""
        target_bases = "BaseA"
        result = InheritanceAnalyzer.get_last_children(source_code, target_bases)

        self.assertEqual(result, ["Final"])


if __name__ == "__main__":
    unittest.main()
