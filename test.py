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

    def test_atom_entails(self):
        g = Graph()
        g.entails(g.atom('A', tv=TRUE), g.atom('B'))
        g.entails(g.atom('B'), g.atom('C'))
        self.assertTrue(g.eval(g.atom('B'), []))
        self.assertTrue(g.eval(g.atom('C'), []))
        self.assertRaises(IndeterminateException, lambda: g.eval(g.atom('F'), []))
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
        self.assertEqual(g.eval(g.atom('C'), [g.atom('T')]), F)
        del g
        g = Graph()
        g.entails(g.atom('A', tv=FALSE), g.atom('B'))
        g.entails(g.atom('B'), g.atom('C'))
        self.assertTrue(g.eval(g.atom('C'), [g.atom('A')]))
        del g

    def test_not_entails(self):
        g = Graph()
        g.entails(INot(g.atom('A', tv=FALSE)), g.atom('B'))
        self.assertEqual(g.eval(g.atom('B')), T)
        del g
        g = Graph()
        g.entails(INot(g.atom('A', tv=TRUE)), g.atom('B'))
        self.assertEqual(g.eval(g.atom('B')), F)

    def test_and_entails(self):
        g = Graph()
        g.entails(
            IAnd(g.atom('A', tv=TRUE), g.atom('B', tv=TRUE)),
            g.atom('D')
        )
        self.assertEqual(g.eval(g.atom('D')), T)
        del g
        g = Graph()
        g.entails(
            IAnd(g.atom('A', tv=TRUE), g.atom('B', tv=FALSE)),
            g.atom('D')
        )
        self.assertEqual(g.eval(g.atom('D')), F)
        del g
        g = Graph()
        g.entails(
            IAnd(g.atom('A', tv=TRUE), g.atom('B')),
            g.atom('D')
        )
        self.assertRaises(IndeterminateException, lambda: g.eval(g.atom('D')))

    def test_or_entails(self):
        g = Graph()
        g.entails(
            IOr(g.atom('A', tv=TRUE), g.atom('B', tv=FALSE)),
            g.atom('D')
        )
        self.assertEqual(g.eval(g.atom('D')), T)
        del g
        g = Graph()
        g.entails(
            IOr(g.atom('A', tv=FALSE), g.atom('B', tv=FALSE)),
            g.atom('D')
        )
        self.assertEqual(g.eval(g.atom('D')), F)
        del g
        g = Graph()
        g.entails(
            IOr(g.atom('A'), g.atom('B')),
            g.atom('D')
        )
        self.assertRaises(IndeterminateException, lambda: g.eval(g.atom('D')))

    def test_and_as_concequent(self):
        g = Graph()
        g.entails(g.atom('A', tv=TRUE), OAnd(
            g.atom('B'), g.atom('C')
        ))
        self.assertEqual(g.eval(g.atom('B')), T)
        del g
        g = Graph()
        g.entails(g.atom('A', tv=FALSE), OAnd(
            g.atom('B'), g.atom('C')
        ))
        self.assertEqual(g.eval(g.atom('B')), F)
        del g

    def test_not_as_concequent(self):
        g = Graph()
        g.entails(g.atom('A', tv=TRUE), ONot(g.atom('C')))
        self.assertEqual(g.eval(g.atom('C')), F)

    def test_or_as_concequent(self):
        g = Graph()
        g.entails(g.atom('A', tv=FALSE), OOr(
            g.atom('B'), g.atom('C')
        ))
        self.assertEqual(g.eval(g.atom('B')), F)
        del g
        g = Graph()
        g.entails(g.atom('A', tv=T), OOr(
            g.atom('B'), g.atom('C', tv=F)
        ))
        self.assertEqual(g.eval(g.atom('B')), T)
        del g
        g = Graph()
        g.entails(g.atom('A', tv=T), OOr(
            g.atom('B'), g.atom('C', tv=T)
        ))
        self.assertRaises(IndeterminateException, lambda: g.eval(g.atom('B')))
        del g
        g = Graph()
        g.entails(g.atom('A', tv=T), ONot(g.atom('C')))
        g.entails(g.atom('A'), OOr(
            g.atom('B'), g.atom('C')
        ))
        self.assertEqual(g.eval(g.atom('B')), T)


if __name__ == "__main__":
    unittest.main()
