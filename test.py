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
        # self.assertRaises(IndeterminateException, lambda: g.eval(g.atom('F'), []))
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
        self.assertEqual(g.eval(g.atom('C'), [g.atom('A')]), T)
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
        del g
        g = Graph()
        g.entails(
            IAnd(g.atom('A'), g.atom('B')),
            g.atom('D')
        )
        self.assertEqual(g.eval(g.atom('D'), [g.atom('A'), g.atom('B')]), T)

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

    def test_xor_entails(self):
        def make_graph():
            g = Graph()
            g.entails(IXor(g.atom('A', tv=FALSE), g.atom('B', tv=FALSE)), g.atom('C'))
            return g
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('C'), [])
        , F)
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('C'), [g.atom('A')])
        , T)
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('C'), [g.atom('B')])
        , T)
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('C'), [g.atom('A'), g.atom('B')])
        , F)

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

    def test_xor_as_concequent(self):
        def make_graph(a=I, b=I, c=I):
            g = Graph()
            g.entails(g.atom('A', tv=a), OXor(g.atom('B', tv=b), g.atom('C', tv=c)))
            return g
        g = make_graph(I, I, F)
        self.assertEqual(
            g.eval(g.atom('B'), [g.atom('A')])
        , T)
        g = make_graph(I, F, I)
        self.assertEqual(
            g.eval(g.atom('C'), [g.atom('A')])
        , T)
        g = make_graph(I, F, I)
        self.assertEqual(
            g.eval(g.atom('C'), [])
        , I)
        g = make_graph(F, F, I)
        self.assertEqual(
            g.eval(g.atom('C'), [])
        , F)
        g = make_graph(F, T, I)
        self.assertEqual(
            g.eval(g.atom('C'), [])
        , T)

    def test_entails_chain_and(self):
        g = Graph()
        g.entails(g.atom('A'), g.atom('A1'))
        g.entails(g.atom('A'), g.atom('A2'))
        g.entails(g.atom('A1'), g.atom('B'))
        g.entails(g.atom('A2'), g.atom('C'))
        g.entails(node.IAnd(g.atom('B'), g.atom('C')), g.atom('D'))
        self.assertEqual(g.eval(g.atom('D'), [g.atom('A')]), T)

    def test_and_antecedent_and_concequent(self):
        g = Graph()
        g.entails(g.atom('B'), g.atom('A'))
        g.entails(IAnd(g.atom('D'), g.atom('E')), g.atom('B'))
        g.entails(IAnd(g.atom('G'), g.atom('H')), g.atom('F'))
        g.entails(IAnd(g.atom('I'), g.atom('J')), g.atom('G'))
        g.entails(g.atom('G'), g.atom('H'))
        g.entails(IAnd(g.atom('L'), g.atom('M')), g.atom('K'))
        g.entails(IAnd(g.atom('O', tv=FALSE), g.atom('P')), OAnd(g.atom('L'), g.atom('N')))
        g.entails(g.atom('N'), g.atom('M'))
        self.assertEqual(g.eval(g.atom('A'), [
            g.atom('D'),
            g.atom('E'),
            g.atom('I'),
            g.atom('J'),
            g.atom('O'),
            g.atom('P'),
        ]), T)
        self.assertEqual(g.eval(g.atom('F')), T)
        self.assertEqual(g.eval(g.atom('P')), T)
        self.assertEqual(g.eval(g.atom('K')), T)
        del g
        g = Graph()
        g.entails(g.atom('B'), g.atom('A'))
        g.entails(IAnd(g.atom('D'), g.atom('E')), g.atom('B'))
        g.entails(IAnd(g.atom('G'), g.atom('H')), g.atom('F'))
        g.entails(IAnd(g.atom('I'), g.atom('J')), g.atom('G'))
        g.entails(g.atom('G'), g.atom('H'))
        g.entails(IAnd(g.atom('L'), g.atom('M')), g.atom('K'))
        g.entails(IAnd(g.atom('O', tv=FALSE), g.atom('P')), OAnd(g.atom('L'), g.atom('N')))
        g.entails(g.atom('N'), g.atom('M'))
        self.assertEqual(g.eval(g.atom('A'), [
            g.atom('D'),
            g.atom('E'),
            g.atom('I'),
            g.atom('J'),
            g.atom('P'),
        ]), T)
        self.assertEqual(g.eval(g.atom('F')), T)
        self.assertEqual(g.eval(g.atom('P')), T)
        self.assertEqual(g.eval(g.atom('K')), F)

    def test_or_antecedent(self):
        def make_graph():
            g = Graph()
            g.entails(IAnd(g.atom('B'), g.atom('C')), g.atom('A'))
            g.entails(IOr(g.atom('D', tv=FALSE), g.atom('E', tv=FALSE)), g.atom('B'))
            g.entails(g.atom('B'), g.atom('C'))
            return g
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('A'), [])
        , F)
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('A'), [g.atom('D')])
        , T)
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('A'), [g.atom('E')])
        , T)
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('A'), [g.atom('D'), g.atom('E')])
        , T)

    def test_xor(self):
        def make_graph(b=I, c=I):
            g = Graph()
            g.entails(IOr(g.atom('B'), g.atom('C')), g.atom('A'))
            g.entails(IXor(g.atom('D', tv=F), g.atom('E', tv=F)), g.atom('B'))
            g.entails(g.atom('B'), g.atom('C'))
            return g
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('A'), [])
        , F)
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('B'), [g.atom('D')])
        , T)
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('A'), [g.atom('E')])
        , T)
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('A'), [g.atom('D'), g.atom('E')])
        , F)

    def test_negations(self):
        def make_graph():
            g = Graph()
            g.entails(IAnd(g.atom('B', tv=FALSE), INot(g.atom('C', tv=FALSE))), g.atom('A'))
            return g
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('A'), [])
        , F)
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('A'), [g.atom('B')])
        , T)
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('A'), [g.atom('C')])
        , F)
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('A'), [g.atom('B'), g.atom('C')])
        , F)

    def test_loop(self):
        pass

    def test_multiple_rules(self):
        def make_graph():
            g = Graph()
            g.entails(g.atom('B'), g.atom('A'))
            g.entails(g.atom('C'), g.atom('A'))
            return g
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('A'), [])
        , I)
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('A'), [g.atom('B')])
        , T)
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('A'), [g.atom('C')])
        , T)
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('A'), [g.atom('B'), g.atom('C')])
        , T)

if __name__ == "__main__":
    unittest.main()

