def eval_node(node, child, skip=None):
    if isinstance(node, OutputNode):
        return node.eval_child(child)
    return node.eval(skip=skip)

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

    def eval(self, verbose=False, skip=None):
        """
        Get this atom's truth value.
        If not lazy, Recursively evaluate this atom's truth value based on its inputs
        params:
            verbose: display reasoning
            skip: None or Node to be skiped. Used by Onodes
        """
        if self._lazy:
            return self._tv
        def do_eval():
            for i in self._inputs:
                if skip and i is skip:
                    continue
                if eval_node(i, self):
                    return True
            return False
        self._tv = do_eval()
        self._lazy = True
        return self._tv

    def reset(self):
        self._tv = False
        self._lazy = False

    def __str__(self):
        return self.name

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

    def eval(self, verbose=False, skip=None):
        if skip and self.i is skip:
            return False
        return not eval_node(self.i, self)

    def __str__(self):
        return "not({})".format(self.i)

class IOr(BinaryInputNode):
    def eval(self, verbose=False, skip=None):
        if skip:
            return eval_node(self.i1, self) if skip is self.i2 else eval_node(self.i2, self)
        return eval_node(self.i1, self) or eval_node(self.i2, self)

    def __str__(self):
        return "({} and {})".format(self.i1, self.i2)

class IAnd(BinaryInputNode):
    def eval(self, verbose=False, skip=None):
        if skip:
            return eval_node(self.i1, self) if skip is self.i2 else eval_node(self.i2, self)
        return eval_node(self.i1, self) and eval_node(self.i2, self)

    def __str__(self):
        return "({} or {})".format(self.i1, self.i2)


class IXor(BinaryInputNode):
    def eval(self, verbose=False, skip=None):
        if skip:
            return eval_node(self.i1, self) if skip is self.i2 else eval_node(self.i2, self)
        t1, t2 = eval_node(self.i1, self), eval_node(self.i2, self)
        if t1 != t2 and (t1 or t2):
            return True

    def __str__(self):
        return "({} xor {})".format(self.i1, self.i2)

class BinaryOutputNode(OutputNode):
    """Node with two outputs, two inputs"""
    def __init__(self, o1, o2):
        self.o1, self.o2 = o1, o2
        self.i = None
        o1.add_input(self)
        o2.add_input(self)

    def add_input(self, i):
        self.i = i

class ONot(OutputNode):
    def __init__(self, o):
        self.o = o
        self.i = None
        o.add_input(self)

    def add_input(self, i):
        self.i = i

    def eval_child(self, child, verbose=False):
        return not eval_node(self.i, self)

    def __str__(self):
        return "not({})".format(self.i)



class OAnd(BinaryOutputNode):
    def eval_child(self, child, verbose=False):
        # assert child is self.o1 or child is self.o2
        return eval_node(self.i, self)

class OOr(BinaryOutputNode):
    def eval_child(self, child, verbose=False):
        # assert child is self.o1 or child is self.o2
        if not eval_node(self.i, self):
            return False
        other = self.o1 if child is self.o2 else self.o2
        if eval_node(other, self, skip=self) is False:
            return True
        return False

class OXor(BinaryOutputNode):
    def eval_child(self, child, verbose=False):
        # assert child is self.o1 or child is self.o2
        other = self.o1 if child is self.o2 else self.o2
        other_tv = eval_node(other, self, self)
        if eval_node(self.i, self):
            return not other_tv
        return other_tv
