from graph import *
from node import *
from error import *
from parser import *
from execute import *
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
        self.assertTrue(parse_rule(g, "A=>B"))

    def test_atom_entails_atom(self):
        g = Graph()
        parse_rule(g, "  AA=>BB   ")
        self.assertEqual(g.eval(g.atom('BB'), [g.atom('AA')]), True)
        self.assertRaises(SyntaxError, lambda: parse_rule(g, "  A A  =>   BB   "))

    def test_xor_entails_atom(self):
        g = Graph()
        parse_rule(g, "  AA     ^   BB  =>   CC   ")
        with g.suppose([g.atom('AA')]):
            self.assertEqual(g.eval(g.atom('CC')), True)
        with g.suppose([g.atom('AA'), g.atom('BB')]):
            self.assertEqual(g.eval(g.atom('CC')), False)
        self.assertRaises(SyntaxError, lambda: parse_rule(g, "  A^^A  =>   BB   "))

    def test_and_entails_atom(self):
        g = Graph()
        parse_rule(g, "  AA     +   BB  =>   CC   ")
        with g.suppose([g.atom('AA')]):
            self.assertEqual(g.eval(g.atom('CC')), False)
        with g.suppose([g.atom('AA'), g.atom('BB')]):
            self.assertEqual(g.eval(g.atom('CC')), True)
        with g.suppose([]):
            self.assertEqual(g.eval(g.atom('CC')), False)

    def test_or_entails_atom(self):
        g = Graph()
        parse_rule(g, "  AA     |   BB  =>   CC   ")
        with g.suppose([g.atom('AA')]):
            self.assertEqual(g.eval(g.atom('CC')), True)
        with g.suppose([g.atom('AA'), g.atom('BB')]):
            self.assertEqual(g.eval(g.atom('CC')), True)
        with g.suppose([]):
            self.assertEqual(g.eval(g.atom('CC')), False)

    def test_atom_entails_xor(self):
        g = Graph()
        parse_rule(g, "  AA  =>     BB  ^   CC   ")
        with g.suppose([g.atom('AA'), g.atom('BB')]):
            self.assertEqual(g.eval(g.atom('CC')), False)

    def test_atom_entails_and(self):
        g = Graph()
        parse_rule(g, "  AA =>   BB  +   CC   ")
        with g.suppose([g.atom('AA')]):
            self.assertEqual(g.eval(g.atom('CC')), True)
        with g.suppose([g.atom('AA')]):
            self.assertEqual(g.eval(g.atom('BB')), True)
        with g.suppose([]):
            self.assertEqual(g.eval(g.atom('CC')), False)

    def test_atom_entails_or(self):
        g = Graph()
        parse_rule(g, "  AA     =>   BB  |   CC   ")
        parse_rule(g, "  AA     =>   !  CC   ")
        with g.suppose([g.atom('AA')]):
            self.assertEqual(g.eval(g.atom('BB')), True)
        with g.suppose():
            self.assertEqual(g.eval(g.atom('CC')), True)

    def test_not_entails_not(self):
        g = Graph()
        parse_rule(g, "  !  AA  =>   ! BB   ")
        with g.suppose([g.atom('AA')]):
            self.assertEqual(g.eval(g.atom('BB')), True)
        with g.suppose([]):
            self.assertEqual(g.eval(g.atom('BB')), False)

    def test_not_entails_atom(self):
        g = Graph()
        parse_rule(g, "  !  AA  =>   BB   ")
        with g.suppose([g.atom('AA')]):
            self.assertEqual(g.eval(g.atom('BB')), False)
        with g.suppose([]):
            self.assertEqual(g.eval(g.atom('BB')), True)

    def test_and_not_entails_atom(self):
        g = Graph()
        parse_rule(g, "  AA     +  !BB  =>   CC   ")
        with g.suppose([g.atom('AA')]):
            self.assertEqual(g.eval(g.atom('CC')), True)
        with g.suppose([g.atom('AA'), g.atom('BB')]):
            self.assertEqual(g.eval(g.atom('CC')), False)
        with g.suppose([]):
            self.assertEqual(g.eval(g.atom('CC')), False)

class TestParseStatement(unittest.TestCase):
    def test_not_a_statement(self):
        g = Graph()
        self.assertIsNone(parse_statement(g, "ABC"))

    def test_empty_statement(self):
        g = Graph()
        self.assertEqual(parse_statement(g, "="), [])

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

class TestExpressions(unittest.TestCase):
    sessions = [
        # ((['a => b'], '=a', '?b'), True),
        # ((['a => b'], '=', '?b'), False),
        # ((['a => b | c'], '=a', '?b'), True),
        # ((['a => b ^ c'], '=c', '?b'), True),
        # ((['a => b + c + d'], '=a', '?b'), True),
        # ((['a => b | c | d'], '=', '?b'), False),
        # ((['a => b | c | d'], '=a', '?b'), False),
        # ((['a => !!b'], '=a', '?b'), True),
        # ((['a => b | c | d', 'a => d'], '=a', '?b'), True),
        ((['a => b | c | d', 'a => d'], '=a', '?c'), True),
        # ((['a => b | c | d', 'a => c'], '=a', '?b'), True),
    ]
    def test_run(self):
        for sess, expected in self.sessions:
            g = Graph()
            rules, statement, query = sess
            for rule in rules:
                parse_rule(g, rule)
            facts = parse_statement(g, statement)
            query_node = parse_query(g, query)[0]
            self.assertEqual(g.eval(query_node, facts), expected,
                "{} {}".format(' '.join(rules), ' '.join(sess[1:])))

if __name__ == "__main__":
    unittest.main()
