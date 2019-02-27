from knowledge_base import KnowledgeBase
from expressions import *
import unittest

class TestAtom(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAtom, self).__init__(*args, **kwargs)
        self.kb = KnowledgeBase({}, [Atom('T')])

    def test_entails_atom(self):
        a = Atom('A')
        self.assertTrue(a.entails(Atom('A'), self.kb))
        self.assertFalse(a.entails(Atom('B'), self.kb))

    def test_entails_not(self):
        a = Atom('A')
        self.assertFalse(a.entails(NotExpression(Atom('A')), self.kb))
    def test_entails_and(self):
        # a = Atom('A')
        # self.assertTrue(a.entails(AndExpression(Atom('A'), Atom('A'))))
        # self.assertFalse(a.entails(Atom('B')))
        pass
    def test_entails_or(self):
        a = Atom('A')
        self.assertTrue(a.entails(OrExpression(Atom('A'), Atom('B')), self.kb))
    def test_entails_xor(self):
        pass

    def test_determines_atom(self):
        a = Atom('A')
        self.assertTrue(a.determines(Atom('A'), self.kb))
        self.assertFalse(a.determines(Atom('B'), self.kb))

    def test_determines_not(self):
        a = Atom('A')
        self.assertTrue(a.determines(Atom('A'), self.kb))
        self.assertFalse(a.determines(Atom('B'), self.kb))

    def test_determines_and(self):
        a = Atom('A')
        self.assertTrue(a.determines(AndExpression(Atom('A'), Atom('T')), self.kb))
        self.assertFalse(a.determines(AndExpression(Atom('A'), Atom('B')), self.kb))

    def test_determines_or(self):
        a = Atom('A')
        self.assertTrue(a.determines(OrExpression(Atom('A'), Atom('B')), self.kb))

    def test_determines_xor(self):
        pass

class TestNotExpression(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestNotExpression, self).__init__(*args, **kwargs)
        self.kb = KnowledgeBase({}, [Atom('T')])

    def test_entails_atom(self):
        a = NotExpression(Atom('A'))
        self.assertFalse(a.entails(Atom('A'), self.kb))

    def test_entails_not(self):
        a = NotExpression(Atom('A'))
        self.assertTrue(a.entails(NotExpression(Atom('A')), self.kb))

    def test_entails_and(self):
        a = NotExpression(Atom('A'))
        self.assertFalse(a.entails(AndExpression(Atom('A'), Atom('B')), self.kb))
        self.assertTrue(a.entails(AndExpression(NotExpression(Atom('A')), Atom('T')), self.kb))

    def test_entails_or(self):
        a = NotExpression(Atom('A'))
        self.assertTrue(a.entails(OrExpression(Atom('A'), Atom('T')), self.kb))
        self.assertFalse(a.entails(OrExpression(Atom('A'), Atom('B')), self.kb))
    def test_entails_xor(self):
        pass

    def test_determines_atom(self):
        a = NotExpression(Atom('A'))
        self.assertTrue(a.determines(Atom('A'), self.kb))
        self.assertFalse(a.determines(Atom('B'), self.kb))

    def test_determines_not(self):
        a = NotExpression(Atom('A'))
        self.assertTrue(a.determines(Atom('A'), self.kb))
        self.assertFalse(a.determines(Atom('B'), self.kb))

    def test_determines_and(self):
        a = NotExpression(Atom('A'))
        self.assertTrue(a.determines(AndExpression(Atom('A'), Atom('T')), self.kb))
        self.assertFalse(a.determines(AndExpression(Atom('A'), Atom('B')), self.kb))

    def test_determines_or(self):
        a = NotExpression(Atom('A'))
        self.assertTrue(a.determines(OrExpression(Atom('A'), Atom('B')), self.kb))
        self.assertFalse(a.determines(OrExpression(Atom('B'), Atom('C')), self.kb))

    def test_determines_xor(self):
        pass

class TestAndExpression(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAndExpression, self).__init__(*args, **kwargs)
        self.kb = KnowledgeBase({}, [Atom('T')])

    def test_entails_atom(self):
        a = AndExpression(Atom('A'), Atom('B'))
        self.assertTrue(a.entails(Atom('A'), self.kb))
        self.assertTrue(a.entails(Atom('B'), self.kb))
        self.assertFalse(a.entails(Atom('C'), self.kb))

    def test_entails_not(self):
        a = AndExpression(Atom('A'), NotExpression(Atom('B')))
        self.assertFalse(a.entails(NotExpression(Atom('A')), self.kb))
        self.assertTrue(a.entails(NotExpression(Atom('B')), self.kb))

    def test_entails_and(self):
        a = AndExpression(Atom('A'), Atom('B'))
        self.assertTrue(a.entails(AndExpression(Atom('B'), Atom('A')), self.kb))
        # self.assertTrue(a.entails(AndExpression(NotExpression(Atom('A')), Atom('T')), self.kb))
        # self.assertFalse(a.entails(AndExpression(NotExpression(Atom('B')), Atom('F')), self.kb))
        # self.assertTrue(a.entails(AndExpression(NotExpression(Atom('T')), Atom('A')), self.kb))
        # self.assertFalse(a.entails(AndExpression(NotExpression(Atom('F')), Atom('B')), self.kb))
        self.assertFalse(a.entails(AndExpression(NotExpression(Atom('A')), Atom('X')), self.kb))

    def test_entails_or(self):
        a = AndExpression(Atom('A'), Atom('B'))
        self.assertTrue(a.entails(OrExpression(Atom('A'), Atom('T')), self.kb))
        self.assertFalse(a.entails(OrExpression(Atom('A'), Atom('B')), self.kb))
    def test_entails_xor(self):
        pass

    # def test_determines_atom(self):
    #     a = NotExpression(Atom('A'))
    #     self.assertTrue(a.determines(Atom('A'), self.kb))
    #     self.assertFalse(a.determines(Atom('B'), self.kb))

    # def test_determines_not(self):
    #     a = NotExpression(Atom('A'))
    #     self.assertTrue(a.determines(Atom('A'), self.kb))
    #     self.assertFalse(a.determines(Atom('B'), self.kb))

    # def test_determines_and(self):
    #     a = NotExpression(Atom('A'))
    #     self.assertTrue(a.determines(AndExpression(Atom('A'), Atom('T')), self.kb))
    #     self.assertFalse(a.determines(AndExpression(Atom('A'), Atom('B')), self.kb))

    # def test_determines_or(self):
    #     a = NotExpression(Atom('A'))
    #     self.assertTrue(a.determines(OrExpression(Atom('A'), Atom('B')), self.kb))
    #     self.assertFalse(a.determines(OrExpression(Atom('B'), Atom('C')), self.kb))

    # def test_determines_xor(self):
    #     pass

if __name__ == "__main__":
    unittest.main()
