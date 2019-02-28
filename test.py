from graph import *
from node import *
from error import *
import unittest

class TestGraph(unittest.TestCase):
    def test_atom_cache(self):
        g = Graph()
        a = g.atom('A')
        b = g.atom('B')
        self.assertIsNot(a ,b)
        self.assertIs(a, g.atom('A'))
        self.assertIs(b, g.atom('B'))
        self.assertIs(g.atom('C'), g.atom('C'))

    def test_atom_entails_true(self):
        g = Graph()
        g.entails(g.atom('A', tv=TRUE), g.atom('B'))
        g.entails(g.atom('B'), g.atom('C'))
        self.assertTrue(g.eval(g.atom('B'), []))
        self.assertTrue(g.eval(g.atom('C'), []))
        self.assertFalse(g.eval(g.atom('F'), []))
        del g
        g = Graph()
        g.entails(g.atom('A', tv=TRUE), g.atom('B'))
        self.assertTrue(
            g.eval(
                g.entails(
                    g.entails(
                        g.atom('B'), g.atom('C')
                    ),
                    g.atom('C')
                ),
            [])
        )
        del g
        g = Graph()
        g.entails(g.atom('A', tv=FALSE), g.atom('B'))
        g.entails(g.atom('B'), g.atom('C'))
        self.assertTrue(g.eval(g.atom('C'), [g.atom('A')]))
        self.assertFalse(g.eval(g.atom('C'), [g.atom('T')]))
        del g

if __name__ == "__main__":
    unittest.main()
