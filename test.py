from KnowledgeBase import KnowledgeBase
from expressions import Atom, AndExpression, NotExpression
import unittest

class TestBasicKnowledgeBase(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()
