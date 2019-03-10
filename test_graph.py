from graph import *
import unittest

class TestGraph(unittest.TestCase):
    def test_atom(self):
        g = Graph()
        self.assertIs(g.atom('a'), g.atom('a'))
        self.assertIsNot(g.atom('b'), g.atom('a'))

    def test_entails_atom(self):
        g = Graph()
        a = g.atom('a')
        b = g.atom('b')
        g.entails(a, b)
        with g.suppose([g.atom('a')]):
            self.assertTrue(g.eval(b))
            self.assertTrue(b.eval())

    def test_entails_and(self):
        g = Graph()
        a = g.atom('a')
        b = g.atom('b')
        c = g.atom('c')
        iand = node.IAnd(a, b)
        g.entails(iand, c)
        with g.suppose([g.atom('a'), g.atom('b')]):
            self.assertTrue(g.eval(c))

if __name__ == "__main__":
    unittest.main()
