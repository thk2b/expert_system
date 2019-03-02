from graph import *
from node import *
from error import *
from parser import *
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
        self.assertEqual(g.eval(g.atom('B'), []), T)
        self.assertEqual(g.eval(g.atom('C'), []), T)
        self.assertEqual(g.eval(g.atom('F'), []), F)
        del g
        g = Graph()
        g.entails(g.atom('A'), g.atom('B'))
        g.entails(g.atom('B'), g.atom('C'))
        self.assertEqual(g.eval(g.atom('C'), [g.atom('T')]), F)
        del g
        g = Graph()
        g.entails(g.atom('A'), g.atom('B'))
        g.entails(g.atom('B'), g.atom('C'))
        self.assertEqual(g.eval(g.atom('C'), [g.atom('A')]), T)
        del g

    def test_not_entails(self):
        g = Graph()
        g.entails(INot(g.atom('A')), g.atom('B'))
        self.assertEqual(g.eval(g.atom('B')), T)
        del g
        g = Graph()
        g.entails(INot(g.atom('A', tv=TRUE)), g.atom('B'))
        self.assertEqual(g.eval(g.atom('B')), F)

    def test_and_entails(self):
        def make_graph(a=I, b=I):
            g = Graph()
            g.entails(
                IAnd(g.atom('A', tv=a), g.atom('B', tv=b)),
                g.atom('D')
            )
            return g
        g = make_graph(T, T)
        self.assertEqual(g.eval(g.atom('D')), T)
        g = make_graph(I, T)
        self.assertEqual(g.eval(g.atom('D')), F)
        g = make_graph(T, I)
        self.assertEqual(g.eval(g.atom('D')), F)
        g = make_graph(I, I)
        self.assertEqual(g.eval(g.atom('D')), F)

    def test_or_entails(self):
        def make_graph(a=I, b=I):
            g = Graph()
            g.entails(
                IOr(g.atom('A', tv=a), g.atom('B', tv=b)),
                g.atom('D')
            )
            return g
        g = make_graph(I, I)
        self.assertEqual(g.eval(g.atom('D')), F)
        g = make_graph(T, I)
        self.assertEqual(g.eval(g.atom('D')), T)
        g = make_graph(I, T)
        self.assertEqual(g.eval(g.atom('D')), T)
        g = make_graph(T, T)
        self.assertEqual(g.eval(g.atom('D')), T)

    def test_xor_entails(self):
        def make_graph(a=I, b=I):
            g = Graph()
            g.entails(
                IXor(g.atom('A', tv=a), g.atom('B', tv=b)),
                g.atom('D')
            )
            return g
        g = make_graph(I, I)
        self.assertEqual(g.eval(g.atom('D')), F)
        g = make_graph(T, I)
        self.assertEqual(g.eval(g.atom('D')), T)
        g = make_graph(I, T)
        self.assertEqual(g.eval(g.atom('D')), T)
        g = make_graph(T, T)
        self.assertEqual(g.eval(g.atom('D')), F)

    def test_and_as_concequent(self):
        def make_graph(a):
            g = Graph()
            g.entails(g.atom('A', tv=a), OAnd(
                g.atom('B'), g.atom('C')
            ))
            return g
        g = make_graph(T)
        self.assertEqual(g.eval(g.atom('B')), T)
        self.assertEqual(g.eval(g.atom('C')), T)
        g = make_graph(F)
        self.assertEqual(g.eval(g.atom('B')), F)
        self.assertEqual(g.eval(g.atom('C')), F)

    def test_not_as_concequent(self):
        def make_graph(a=I):
            g = Graph()
            g.entails(g.atom('A', tv=a), ONot(g.atom('C')))
            return g
        g = make_graph(T)
        self.assertEqual(g.eval(g.atom('C')), F)
        g = make_graph(F)
        self.assertEqual(g.eval(g.atom('C')), T)

    def test_or_as_concequent(self):
        def make_graph(a=I, b=I, c=I):
            g = Graph()
            g.entails(g.atom('A', tv=a), OOr(
                g.atom('B', tv=b), g.atom('C', tv=c)
            ))
            return g
        g = make_graph(F)
        self.assertEqual(g.eval(g.atom('B')), F)
        self.assertEqual(g.eval(g.atom('C')), F)
        g = make_graph(T, F, I)
        self.assertEqual(g.eval(g.atom('C')), T)
        g = make_graph(T, I, F)
        self.assertEqual(g.eval(g.atom('B')), T)
        g = make_graph(T, I, T)
        self.assertEqual(g.eval(g.atom('B')), I)

    def test_xor_as_concequent(self):
        def make_graph(a=I, b=I, c=I):
            g = Graph()
            g.entails(g.atom('A', tv=a), OXor(g.atom('B', tv=b), g.atom('C', tv=c)))
            return g
        g = make_graph(T, I, F)
        self.assertEqual(g.eval(g.atom('B')), T)
        g = make_graph(T, F, I)
        self.assertEqual(g.eval(g.atom('C')), T)

        g = make_graph(F, F, I)
        self.assertEqual(g.eval(g.atom('C')), F)
        g = make_graph(F, F, I)
        self.assertEqual(g.eval(g.atom('C')), F)
        g = make_graph(F, T, I)
        self.assertEqual(g.eval(g.atom('C')), T)

    def test_entails_chain_and(self):
        g = Graph()
        g.entails(g.atom('A'), g.atom('A1'))
        g.entails(g.atom('A'), g.atom('A2'))
        g.entails(g.atom('A1'), g.atom('B'))
        g.entails(g.atom('A2'), g.atom('C'))
        g.entails(node.IAnd(g.atom('B'), g.atom('C')), g.atom('D'))
        self.assertEqual(g.eval(g.atom('D'), [g.atom('A')]), T)

    def test_and_antecedent_and_concequent(self): #TODO: refactor
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
            g.entails(IOr(g.atom('D'), g.atom('E')), g.atom('B'))
            g.entails(g.atom('B'), g.atom('C'))
            return g
        g = make_graph()
        self.assertEqual(g.eval(g.atom('A'), []), F)
        g = make_graph()
        self.assertEqual(g.eval(g.atom('A'), [g.atom('D')]), T)
        g = make_graph()
        self.assertEqual(g.eval(g.atom('A'), [g.atom('E')]), T)
        g = make_graph()
        self.assertEqual(g.eval(g.atom('A'), [g.atom('D'), g.atom('E')]), T)

    def test_xor(self):
        def make_graph(b=I, c=I):
            g = Graph()
            g.entails(IOr(g.atom('B'), g.atom('C')), g.atom('A'))
            g.entails(IXor(g.atom('D', tv=F), g.atom('E', tv=F)), g.atom('B'))
            g.entails(g.atom('B'), g.atom('C'))
            return g
        g = make_graph()
        self.assertEqual(g.eval(g.atom('A'), []), F)
        g = make_graph()
        self.assertEqual(g.eval(g.atom('B'), [g.atom('D')]), T)
        g = make_graph()
        self.assertEqual(g.eval(g.atom('A'), [g.atom('E')]), T)
        g = make_graph()
        self.assertEqual(g.eval(g.atom('A'), [g.atom('D'), g.atom('E')]), F)

    def test_negations(self):
        def make_graph():
            g = Graph()
            g.entails(IAnd(g.atom('B'), INot(g.atom('C'))), g.atom('A'))
            return g
        g = make_graph()
        self.assertEqual(g.eval(g.atom('A'), []), F)
        g = make_graph()
        self.assertEqual(g.eval(g.atom('A'), [g.atom('B')]), T)
        g = make_graph()
        self.assertEqual(g.eval(g.atom('A'), [g.atom('C')]), F)
        g = make_graph()
        self.assertEqual(g.eval(g.atom('A'), [g.atom('B'), g.atom('C')]), F)

    def test_loop(self):
        g = Graph()
        self.assertRaises(ValueError, lambda: g.entails(g.atom('A'), g.atom('A')))

    def test_multiple_rules(self):
        def make_graph():
            g = Graph()
            g.entails(g.atom('B'), g.atom('A'))
            g.entails(g.atom('C'), g.atom('A'))
            return g
        g = make_graph()
        self.assertEqual(g.eval(g.atom('A'), []), F)
        g = make_graph()
        self.assertEqual(g.eval(g.atom('A'), [g.atom('B')]), T)
        g = make_graph()
        self.assertEqual(g.eval(g.atom('A'), [g.atom('C')]), F) # B is marked as false, was indeterminate
        g = make_graph()
        self.assertEqual(g.eval(g.atom('A'), [g.atom('B'), g.atom('C')]), T)

    def test_nested_and_or(self):
        def make_graph():
            g = Graph()
            g.entails(
                IOr(g.atom('A'), g.atom('C')),
                ONot(g.atom('E'))
            )
            g.entails(
                IOr(
                    IAnd(g.atom('A'), g.atom('B')),
                    g.atom('C')
                ),
                OOr(
                    g.atom('D'),
                    g.atom('E')
                )
            )
            return g
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('D'), [g.atom('A'), g.atom('B')])
        , T)
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('D'), [g.atom('C')])
        , T)
        g = make_graph()
        self.assertEqual(
            g.eval(g.atom('D'), [])
        , F)

    def test_not_and_not_and(self):
        def make_graph():
            g = Graph()
            g.entails(
                INot(IAnd(g.atom('A'), g.atom('B'))),
                ONot(OAnd(g.atom('C'), g.atom('D')))
            )
            return g
        g = make_graph()
        self.assertEqual(g.eval(g.atom('C')), F)
        g = make_graph()
        self.assertEqual(g.eval(g.atom('C'), [g.atom('A'), g.atom('B')]), T)
        g = make_graph()
        self.assertEqual(g.eval(g.atom('C'), [g.atom('A')]), F)
    
    def test_nested_oand(self):
        def make_graph():
            g = Graph()
            g.entails(g.atom('A'),
                OAnd(
                    OAnd(g.atom('B'), g.atom('C')),
                    g.atom('D')
                )
            )
            return g
        g = make_graph()
        self.assertEqual(g.eval(g.atom('B')), F)
        g = make_graph()
        self.assertEqual(g.eval(g.atom('B'), [g.atom('A')]), T)

    def test_nested_oor(self):
        def make_graph():
            g = Graph()
            g.entails(g.atom('A'),
                OOr(
                    OOr(g.atom('B'), g.atom('C')),
                    g.atom('D')
                )
            )
            g.entails(g.atom('A'), ONot(OAnd(g.atom('C'), g.atom('D'))))
            return g
        g = make_graph()
        self.assertEqual(g.eval(g.atom('B'), [g.atom('A')]), T)
        g = make_graph()
        self.assertEqual(g.eval(g.atom('B'), []), F)

    def test_eval_and(self):
        def make_graph():
            g = Graph()
            g.entails(g.atom('A'), g.atom('B'))
            return g
        g = make_graph()
        self.assertEqual(g.eval(IAnd(g.atom('A'), g.atom('B'))), F)
        g = make_graph()
        self.assertEqual(g.eval(IAnd(g.atom('A'), g.atom('B')), [g.atom('A')]), T)

    def test_eval_or(self):
        g = Graph()
        self.assertEqual(g.eval(IOr(g.atom('A'), g.atom('B'))), F)
        g = Graph()
        self.assertEqual(g.eval(IOr(g.atom('A'), g.atom('B')), [g.atom('A')]), T)
        g = Graph()
        self.assertEqual(g.eval(IOr(g.atom('A'), g.atom('B')), [g.atom('B')]), T)
        g = Graph()
        self.assertEqual(g.eval(IOr(g.atom('A'), g.atom('B')), [g.atom('A'), g.atom('B')]), T)

    def test_eval_xor(self):
        g = Graph()
        self.assertEqual(g.eval(IXor(g.atom('A'), g.atom('B'))), F)
        g = Graph()
        self.assertEqual(g.eval(IXor(g.atom('A'), g.atom('B')), [g.atom('A')]), T)
        g = Graph()
        self.assertEqual(g.eval(IXor(g.atom('A'), g.atom('B')), [g.atom('B')]), T)
        g = Graph()
        self.assertEqual(g.eval(IXor(g.atom('A'), g.atom('B')), [g.atom('A'), g.atom('B')]), F)

class TestSplit(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(split("ab cd ef", "cd"), ("ab", "ef"))
        self.assertEqual(split("ab c d ef", "cd"), (None, None))
        self.assertEqual(split("ab cd ef cd", "cd"), ("ab", "ef cd"))
        self.assertEqual(split("     ab   cd     ef  ", "cd"), ("ab", "ef"))

    def test_parens(self):
        self.assertEqual(
            split("ab {} cd {} ef".format(terminals['LPAREN'], terminals['RPAREN']), "cd"),
            (None, None)
        )
        self.assertEqual(
            split("ab {}{} cd {}{} cd ef".format(terminals['LPAREN'], terminals['LPAREN'], terminals['RPAREN'], terminals['RPAREN']), "cd"),
            ("ab {}{} cd {}{}".format(terminals['LPAREN'], terminals['LPAREN'], terminals['RPAREN'], terminals['RPAREN']), "ef")
        )

    def test_invalid_parens(self):
        self.assertRaises(SyntaxError, lambda: split("()(()", "a"))
        self.assertRaises(SyntaxError, lambda: split("())()", "a"))
        split("((())())", "a")

class TestParseRule(unittest.TestCase):
    def test_return_value(self):
        g = Graph()
        self.assertFalse(parse_rule(g, "=ABC"))
        self.assertTrue(parse_rule(g, "A->B"))

    def test_atom_entails_atom(self):
        g = Graph()
        parse_rule(g, "  AA->BB   ")
        self.assertEqual(g.eval(g.atom('BB'), [g.atom('AA')]), T)
        self.assertRaises(SyntaxError, lambda: parse_rule(g, "  A A  ->   BB   "))

    def test_xor_entails_atom(self):
        g = Graph()
        parse_rule(g, "  AA     ^   BB  ->   CC   ")
        with g.suppose([g.atom('AA')]):
            self.assertEqual(g.eval(g.atom('CC')), T)
        with g.suppose([g.atom('AA'), g.atom('BB')]):
            self.assertEqual(g.eval(g.atom('CC')), F)
        self.assertRaises(SyntaxError, lambda: parse_rule(g, "  A^^A  ->   BB   "))

    def test_and_entails_atom(self):
        g = Graph()
        parse_rule(g, "  AA     +   BB  ->   CC   ")
        with g.suppose([g.atom('AA')]):
            self.assertEqual(g.eval(g.atom('CC')), F)
        with g.suppose([g.atom('AA'), g.atom('BB')]):
            self.assertEqual(g.eval(g.atom('CC')), T)
        with g.suppose([]):
            self.assertEqual(g.eval(g.atom('CC')), F)

    def test_or_entails_atom(self):
        g = Graph()
        parse_rule(g, "  AA     |   BB  ->   CC   ")
        with g.suppose([g.atom('AA')]):
            self.assertEqual(g.eval(g.atom('CC')), T)
        with g.suppose([g.atom('AA'), g.atom('BB')]):
            self.assertEqual(g.eval(g.atom('CC')), T)
        with g.suppose([]):
            self.assertEqual(g.eval(g.atom('CC')), F)

    def test_atom_entails_xor(self):
        g = Graph()
        parse_rule(g, "  AA  ->     BB  ^   CC   ")
        with g.suppose([g.atom('AA'), g.atom('BB')]):
            self.assertEqual(g.eval(g.atom('CC')), F)

    def test_atom_entails_and(self):
        g = Graph()
        parse_rule(g, "  AA ->   BB  +   CC   ")
        with g.suppose([g.atom('AA')]):
            self.assertEqual(g.eval(g.atom('CC')), T)
        with g.suppose([g.atom('AA')]):
            self.assertEqual(g.eval(g.atom('BB')), T)
        with g.suppose([]):
            self.assertEqual(g.eval(g.atom('CC')), F)

    def test_atom_entails_or(self):
        g = Graph()
        parse_rule(g, "  AA     ->   BB  |   CC   ")
        parse_rule(g, "  AA     ->   !  CC   ")
        with g.suppose([g.atom('AA')]):
            self.assertEqual(g.eval(g.atom('BB')), T)
        with g.suppose([]):
            self.assertEqual(g.eval(g.atom('CC')), F)

    def test_not_entails_not(self):
        g = Graph()
        parse_rule(g, "  !  AA  ->   ! BB   ")
        with g.suppose([g.atom('AA')]):
            self.assertEqual(g.eval(g.atom('BB')), T)
        with g.suppose([]):
            self.assertEqual(g.eval(g.atom('BB')), F)

    def test_not_entails_atom(self):
        g = Graph()
        parse_rule(g, "  !  AA  ->   BB   ")
        with g.suppose([g.atom('AA')]):
            self.assertEqual(g.eval(g.atom('BB')), F)
        with g.suppose([]):
            self.assertEqual(g.eval(g.atom('BB')), T)

    def test_and_not_entails_atom(self):
        g = Graph()
        parse_rule(g, "  AA     +  !BB  ->   CC   ")
        with g.suppose([g.atom('AA')]):
            self.assertEqual(g.eval(g.atom('CC')), T)
        with g.suppose([g.atom('AA'), g.atom('BB')]):
            self.assertEqual(g.eval(g.atom('CC')), F)
        with g.suppose([]):
            self.assertEqual(g.eval(g.atom('CC')), F)

class TestParseStatement(unittest.TestCase):
    def test_not_a_statement(self):
        g = Graph()
        self.assertIsNone(parse_statement(g, "ABC"))

    def test_compact_atom_list(self):
        g = Graph()
        self.assertEqual(parse_statement(g, "=A       BC"), [
            g.atom('A'), g.atom('B'), g.atom('C')
        ])

    def test_separated_atom_list(self):
        g = Graph()
        self.assertEqual(parse_statement(g, "=A, B,  C"), [
            g.atom('A'), g.atom('B'), g.atom('C')
        ])

class TestParseQuery(unittest.TestCase):
    def test_not_a_query(self):
        g = Graph()
        self.assertIsNone(parse_query(g, "ABC"))

    def test_compact_atom_list(self):
        g = Graph()
        self.assertEqual(parse_query(g, "?A       BC"), [
            g.atom('A'), g.atom('B'), g.atom('C')
        ])

    def test_separated_atom_list(self):
        g = Graph()
        self.assertEqual(parse_query(g, "?A, B,  C"), [
            g.atom('A'), g.atom('B'), g.atom('C')
        ]) 

if __name__ == "__main__":
    unittest.main()
