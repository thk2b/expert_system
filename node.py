class Node:
    pass

class InputNode(Node):
    pass

class OutputNode(Node):
    pass

class Atom:
    """
    Represents an atomic fact.
    Members:
        name: a unique alphanumeric name
        _lazy: if True, do not recursively evaluate the atom's truth value
        _tv: this atom's truth value.
        _inputs: list of connections to other atoms.
            If an input is true, then this atom is true.
            If all inputs are false, then this atom is false
        _outputs: list of dependent atoms.
    """
    def __init__(self, name, graph=None):
        self.name = name
        self._lazy = False
        self._tv = False
        self._inputs, self._outputs = [], []
        self._graph = graph

    @property
    def tv(self):
        if self._lazy:
            return self._tv
        return self.eval()

    @tv.setter
    def tv(self, tv):
        if self._lazy:
            raise ValueError('cannot set the truth value of a lazy node')
        self._lazy = True
        self._tv = tv

    def add_input(self, i):
        self._inputs.append(i)

    def add_output(self, o):
        self._outputs.append(o)

    def eval(self, verbose=False):
        """
        Get this atom's truth value.
        If not lazy, Recursively evaluate this atom's truth value based on its inputs
        """
        if self._lazy:
            return self._tv
        def eval():
            for i in self._inputs:
                if i.eval():
                    return True
            return False
        self._tv = eval()
        self._lazy = True
        return self._tv

    def reset(self):
        self._tv = False
        self._lazy = False

class BinaryInputNode(InputNode):
    """Node with two inputs, two outputs"""
    def __init__(self, i1, i2):
        self.i1, self.i2 = i1, i2
        self.o = None

    def add_output(self, o):
        self.o = o

class INot(InputNode):
    def __init__(self, i):
        self.i = i
        self.o = None
        i.add_output(self)

    def add_output(self, o):
        self.o = o

    def eval(self, verbose=False):
        return not self.i.eval()

class IOr(BinaryInputNode):
    def eval(self, verbose=False):
        return self.i1.eval() or self.i2.eval()

class IAnd(BinaryInputNode):
    def eval(self, verbose=False):
        return self.i1.eval() and self.i2.eval()

class IXor(BinaryInputNode):
    def eval(self, verbose=False):
        t1, t2 = self.i1.eval(), self.i2.eval()
        if t1 != t2 and (t1 or t2):
            return True

class BinaryOutputNode(OutputNode):
    """Node with two outputs, two inputs"""
    def __init__(self, o1, o2):
        self.o1, self.o2 = o1, o2
        self.i = None
        o1.add_output(self)
        o2.add_output(self)

    def add_input(self, o):
        self.i = i
