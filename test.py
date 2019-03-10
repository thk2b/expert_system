import unittest
from node2 import *


class TestAtom(unittest.TestCase):
    def test_basic_1(self):
        a = Atom('a')
        b = Atom('b')
        c = Atom('c')
        a.add_output(b)
        b.add_output(c)
        b.add_input(a)
        c.add_input(b)
        a.tv = True
        self.assertTrue(c.tv)

    def test_basic_2(self):
        a = Atom('a')
        b = Atom('b')
        c = Atom('c')
        a.add_output(b)
        b.add_output(c)
        b.add_input(a)
        c.add_input(b)
        self.assertFalse(c.tv)

class TestINot(unittest.TestCase):
    def test_basic_1(self):
        truth_table = {
            (False,): True,
            (True,): False,
        }
        def get_node(tv):
            a = Atom('a')
            a.tv = tv
            return INot(a)
        for input, output in truth_table.items():
            inot = get_node(input[0])
            b = Atom('b')
            inot.add_output(b)
            b.add_input(inot)
            self.assertEqual(b.eval(), output)

class TestIAnd(unittest.TestCase):
    def test_basic_1(self):
        truth_table = {
            (False, False): False,
            (True, False): False,
            (False, True): False,
            (True, True): True,
        }
        def get_node(tv1, tv2):
            a = Atom('a')
            a.tv = tv1
            b = Atom('b')
            b.tv = tv2
            return IAnd(a, b)
        for input, output in truth_table.items():
            iand = get_node(input[0], input[1])
            c = Atom('c')
            iand.add_output(c)
            c.add_input(iand)
            self.assertEqual(c.eval(), output)

class TestIOr(unittest.TestCase):
    def test_basic_1(self):
        truth_table = {
            (False, False): False,
            (True, False): True,
            (False, True): True,
            (True, True): True,
        }
        def get_node(tv1, tv2):
            a = Atom('a')
            a.tv = tv1
            b = Atom('b')
            b.tv = tv2
            return IOr(a, b)
        for input, output in truth_table.items():
            iand = get_node(input[0], input[1])
            c = Atom('c')
            iand.add_output(c)
            c.add_input(iand)
            self.assertEqual(c.eval(), output)

class TestIXor(unittest.TestCase):
    def test_basic_1(self):
        truth_table = {
            (False, False): False,
            (True, False): True,
            (False, True): True,
            (True, True): False,
        }
        def get_node(tv1, tv2):
            a = Atom('a')
            a.tv = tv1
            b = Atom('b')
            b.tv = tv2
            return IXor(a, b)
        for input, output in truth_table.items():
            iand = get_node(input[0], input[1])
            c = Atom('c')
            iand.add_output(c)
            c.add_input(iand)
            self.assertEqual(c.eval(), output)

if __name__ == "__main__":
    unittest.main()
