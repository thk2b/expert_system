from KnowledgeBase import KnowledgeBase
from expressions import *
import unittest

class TestKnowledgeBase(unittest.TestCase):
    def test_simple_backwards_chaining(self):
        """A -> B, X -> D, B -> C, =A, ?ACD"""
        rules = {
            Atom('A'): [Atom('B')],
            Atom('X'): [Atom('D')],
            Atom('B'): [Atom('C')]
        }
        facts = [
            Atom('A')
        ]
        kb = KnowledgeBase(rules, facts)
        self.assertTrue(kb.query(Atom('A')))
        self.assertTrue(kb.query(Atom('C')))
        self.assertFalse(kb.query(Atom('D')))

    def test_multiple_rules_same_antecedent(self):
        """A -> B, A -> C, =A, ?ABC"""
        rules = {
            Atom('A'): [Atom('B')],
            Atom('A'): [Atom('C')],
        }
        facts = [
            Atom('A')
        ]
        kb = KnowledgeBase(rules, facts)
        self.assertTrue(kb.query(Atom('A')))
        self.assertTrue(kb.query(Atom('B')))
        self.assertTrue(kb.query(Atom('C')))

    def test_not_expression_as_antecedent(self):
        """!A -> B, =, ?AB"""
        rules = {
            NotExpression(Atom('A')): [Atom('B')]
        }
        facts = []
        kb = KnowledgeBase(rules, facts)
        self.assertFalse(kb.query(Atom('A')))
        self.assertTrue(kb.query(Atom('B')))

    def test_and_expression_as_antecedent(self):
        """A + B -> C, =AB, ?ABC"""
        rules = {
            AndExpression(Atom('A'), Atom('B')): [Atom('C')]
        }
        facts = [
            Atom('A'), Atom('B')
        ]
        kb = KnowledgeBase(rules, facts)
        self.assertTrue(kb.query(Atom('A')))
        self.assertTrue(kb.query(Atom('B')))
        self.assertTrue(kb.query(Atom('C')))

    def test_nested_expression_as_antecedent(self):
        """A + B + C -> D, =ABC, ?D"""
        rules = {
            AndExpression(AndExpression(Atom('A'), Atom('B')), Atom('C')): [Atom('D')]
        }
        facts = [
            Atom('A'), Atom('B'), Atom('C')
        ]
        kb = KnowledgeBase(rules, facts)
        self.assertTrue(kb.query(Atom('D')))

    def test_xor_expression_as_antecedent(self):
        """A ^ B -> C1, A ^ A -> C2, =A, ?A C1 C2"""
        rules = {
            XorExpression(Atom('A'), Atom('B')): [Atom('C1')],
            XorExpression(Atom('A'), Atom('A')): [Atom('C2')]
        }
        facts = [
            Atom('A')
        ]
        kb = KnowledgeBase(rules, facts)
        self.assertTrue(kb.query(Atom('A')))
        self.assertTrue(kb.query(Atom('C1')))
        self.assertFalse(kb.query(Atom('C2')))

    def test_or_expression_as_antecedent(self):
        """A | B -> C, =A, ?ABC"""
        rules = {
            OrExpression(Atom('A'), Atom('B')): [Atom('C')]
        }
        facts = [
            Atom('A')
        ]
        kb = KnowledgeBase(rules, facts)
        self.assertTrue(kb.query(Atom('A')))
        self.assertFalse(kb.query(Atom('B')))
        self.assertTrue(kb.query(Atom('C')))

    def test_and_expression_as_antecedent_with_rule(self):
        """A + B -> C, A -> B, =A, ?ABC"""
        rules = {
            AndExpression(Atom('A'), Atom('B')): [Atom('C')],
            Atom('A'): [Atom('B')]
        }
        facts = [
            Atom('A')
        ]
        kb = KnowledgeBase(rules, facts)
        self.assertTrue(kb.query(Atom('A')))
        self.assertTrue(kb.query(Atom('B')))
        self.assertTrue(kb.query(Atom('C')))

    def test_or_expression_as_antecedent_with_rule(self):
        """A -> B, B | C -> D, =A, ?BCD"""
        rules = {
            Atom('A'): [Atom('B')],
            OrExpression(Atom('B'), Atom('C')): [Atom('D')],
        }
        facts = [
            Atom('A')
        ]
        kb = KnowledgeBase(rules, facts)
        self.assertTrue(kb.query(Atom('B')))
        self.assertFalse(kb.query(Atom('C')))
        self.assertTrue(kb.query(Atom('D')))

    def test_not_expression_as_concequent(self):
        """A -> !B, =A, ?AB"""
        rules = {
            Atom('A'): [NotExpression(Atom('B'))],
        }
        facts = [
            Atom('A')
        ]
        kb = KnowledgeBase(rules, facts)
        self.assertTrue(kb.query(Atom('A')))
        self.assertFalse(kb.query(Atom('B')))

    def test_or_expression_as_concequent(self):
        """A -> B | C, A -> !B, =A, ?ABC"""
        rules = {
            Atom('A'): [OrExpression(Atom('B'), Atom('C'))],
            Atom('A'): [NotExpression(Atom('B'))]
        }
        facts = [
            Atom('A')
        ]
        kb = KnowledgeBase(rules, facts)
        self.assertTrue(kb.query(Atom('A')))
        self.assertFalse(kb.query(Atom('B')))
        self.assertTrue(kb.query(Atom('C')))

    def test_and_expression_as_concequent(self):
        """A -> B + C, =A, ?ABC"""
        rules = {
            Atom('A'): [AndExpression(Atom('B'), Atom('C'))],
        }
        facts = [
            Atom('A')
        ]
        kb = KnowledgeBase(rules, facts)
        self.assertTrue(kb.query(Atom('A')))
        self.assertTrue(kb.query(Atom('B')))
        self.assertTrue(kb.query(Atom('C')))

    def test_query_expression(self):
        """=AB ?(A+B)"""
        kb = KnowledgeBase({}, [Atom('A'), Atom('B')])
        self.assertFalse(kb.query(NotExpression(Atom('A'))))
        self.assertTrue(kb.query(AndExpression(Atom('A'), Atom('B'))))
        self.assertTrue(kb.query(OrExpression(Atom('A'), Atom('B'))))
        self.assertFalse(kb.query(XorExpression(Atom('A'), Atom('B'))))

    def test_query_expression_with_rules(self):
        """"""
        rules = {
            Atom('A'): Atom('B'),
            Atom('A'): NotExpression('C')
        }
        facts = [
            Atom('A')
        ]
        kb = KnowledgeBase(rules, facts)
        self.assertTrue(XorExpression(Atom('B'), NotExpression('C')))


if __name__ == '__main__':
    unittest.main()
