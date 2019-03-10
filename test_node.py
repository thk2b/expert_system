import unittest
from node import *

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

class TestONot(unittest.TestCase):
    def test_basic_1(self):
        truth_table = {
            False: (True,),
            True: (False,),
        }
        for input, output in truth_table.items():
            a = Atom('a')
            a.tv = input
            b = Atom('b')
            onot = ONot(b)
            a.add_output(onot)
            onot.add_input(a)
            self.assertEqual(b.eval(), output[0])

class TestOAnd(unittest.TestCase):
    def test_basic_1(self):
        truth_table = {
            True: (True, True),
            False: (False, False)
        }
        for input, outputs in truth_table.items():
            a = Atom('a')
            b = Atom('b')
            c = Atom('c')
            a.tv = input
            c.tv = outputs[0]
            oand = OAnd(b, c)
            oand.add_input(a)
            a.add_output(oand)
            self.assertEqual(b.eval(), outputs[1])

    def test_nested(self):
        a = Atom('a')
        b = Atom('b')
        c = Atom('c')
        d = Atom('d')
        e = Atom('e')
        a.tv = True
        oand = OAnd(
            OOr(b, c),
            OOr(d, e)
        )
        oand.add_input(a)
        a.add_output(oand)
        self.assertTrue(b.eval())

class TestOOr(unittest.TestCase):
    def test_basic_1(self):
        truth_table = {
            #truth value of OOr
            True: {
                # truth value of other child: truth value of evaluated child
                False: True,
                True: False
            },
            False: {
                False: False,
                True: False,
            }
        }
        for input, outputs in truth_table.items():
            for other_tv, expected_tv in outputs.items():
                a = Atom('a')
                b = Atom('b')
                c = Atom('c')
                a.tv = input
                c.tv = other_tv
                oor = OOr(b, c)
                oor.add_input(a)
                a.add_output(oor)
                self.assertEqual(b.eval(), expected_tv, "in={} other={} expected={}".format(input, other_tv, expected_tv))

class TestOXor(unittest.TestCase):
    def test_basic_1(self):
        truth_table = {
            True: {
                False: True,
                True: False
            },
            False: {
                False: False,
                True: True,
            }
        }
        for input, outputs in truth_table.items():
            for other_tv, expected_tv in outputs.items():
                a = Atom('a')
                b = Atom('b')
                c = Atom('c')
                a.tv = input
                c.tv = other_tv
                oxor = OXor(b, c)
                oxor.add_input(a)
                a.add_output(oxor)
                self.assertEqual(b.eval(), expected_tv, "in={} other={} expected={}".format(input, other_tv, expected_tv))

if __name__ == "__main__":
    unittest.main()
