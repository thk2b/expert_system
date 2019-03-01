import error
T, I, F = TRUE, INDETERMINATE, FALSE = 1, 0, -1

def bool_to_tv(b):
    return T if b else F

TV_TABLE = {I:'I', T:'T', F:'F'}

class Node:
    """Represents a basic node in the knowledge graph"""
    def __init__(self):
        """
        Args:
        """
        self.skip = False

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

class Atom(Node):
    def __init__(self, name, graph, tv=INDETERMINATE):
        super().__init__()
        self.tv = tv
        self.name = name
        self.graph = graph
        self.inputs = []
        self.outputs = []

    def eval(self, child=None):
        if self.tv != INDETERMINATE:
            return self.tv
        for i in self.inputs:
            if i.skip:
                continue
            tv = i.eval(self)
            if tv != INDETERMINATE:
                self.tv = tv
                return self.tv
        return INDETERMINATE

    def __str__(self):
        return "Atom({})[{}]".format(self.name, TV_TABLE[self.tv])

class INot(Node):
    """Represents a not node in the knowledge graph"""
    def __init__(self, input_node):
        super().__init__()
        if isinstance(input_node, Atom):
            input_node.outputs.append(self)
        else:
            input_node.output = self
        self.input = input_node
        self.output = None

    def eval(self, child=None):
        """
        Evaluate the truth value of this node
            if node is not indeterminate return self.tv
            for each node in self.input if node is not indeterminate return not node.tv
        """
        tv = self.input.eval(self)
        if tv != INDETERMINATE:
            return T if tv is F else F
        return INDETERMINATE

class BinaryInputNode(Node):
    """
    InputNode: has 2 inputs, one output
    """
    def __init__(self, i1, i2, **kwargs):
        super().__init__(**kwargs)
        self.i1, self.i2 = i1, i2
        self.output = None

class IAnd(BinaryInputNode):
    """Represents an and node in the knowledge graph"""
    def eval(self, child=None):
        for i in (self.i1, self.i2):
            if i.skip:
                continue
            tv = i.eval(self)
            if tv == INDETERMINATE:
                return INDETERMINATE
            if tv == FALSE:
                return FALSE
        return TRUE

class IOr(BinaryInputNode):
    """Represents an or node in the knowledge graph"""
    def eval(self, child=None):
        for i in (self.i1, self.i2):
            if i.skip:
                continue
            tv = i.eval(self)
            if tv == TRUE:
                return TRUE
        return FALSE

class IXor(BinaryInputNode):
    def eval(self, child=None):
        for i in (self.i1, self.i2):
            if i.skip:
                continue
            tv = i.eval(self)
            if tv == INDETERMINATE:
                return INDETERMINATE
        if self.i1.tv == self.i2.tv:
            return FALSE
        return TRUE

class ONot(Node):
    """Represents a not node in the knowledge graph"""
    def __init__(self, output_node):
        super().__init__()
        if isinstance(output_node, Atom):
            output_node.inputs.append(self)
        else:
            output_node.input = self
        self.output = output_node
        self.input = None

    def eval(self, child=None):
        tv = self.input.eval(self)
        if tv != INDETERMINATE:
            return T if tv is F else F
        return INDETERMINATE

class BinaryOutputNode(Node):
    """
    OutputNode: has 2 outputs, one input
    """
    def __init__(self, o1, o2, **kwargs):
        super().__init__(**kwargs)
        self.o1, self.o2 = o1, o2
        for o in (o1, o2):
            if isinstance(o, Atom):
                o.inputs.append(self)
            else:
                o.input = self
        self.input = None

class OAnd(BinaryOutputNode):
    def eval(self, child):
        return self.input.eval(self)

class OOr(BinaryOutputNode):
    def eval(self, child):
        if (child is not self.o1) and (child is not self.o2):
            raise ValueError("Child {} is not an output node".format(child))
        if child is None:
            return INDETERMINATE
        tv = self.input.eval(self)
        if tv != TRUE:
            if isinstance(child, Atom):
                child.tv = tv
            return tv
        other = self.o1 if child is self.o2 else self.o2
        self.skip = True
        other_tv = other.eval(None)
        self.skip = False
        if other_tv == FALSE:
            child.tv = TRUE
            return TRUE
        if isinstance(child, Atom):
            child.tv = INDETERMINATE
        return INDETERMINATE

class OXor(BinaryOutputNode):
    def eval(self, child):
        if (child is not self.o1) and (child is not self.o2):
            raise ValueError("Child {} is not an output node".format(child))
        if child is None:
            return INDETERMINATE
        tv = self.input.eval(self)
        if tv == INDETERMINATE:
            if isinstance(child, Atom):
                child.tv = INDETERMINATE
            return INDETERMINATE
        other = self.o1 if child is self.o2 else self.o2
        self.skip = True
        other_tv = other.eval(None)
        self.skip = False
        if other_tv == INDETERMINATE:
            child.tv = INDETERMINATE
            return INDETERMINATE
        if tv == TRUE:
            if other_tv == TRUE:
                if isinstance(child, Atom):
                    child.tv = FALSE
                return FALSE
            child.tv = TRUE
            return TRUE
        if other_tv == TRUE:
            if isinstance(child, Atom):
                child.tv = TRUE
            return TRUE
        if isinstance(child, Atom):
            child.tv = FALSE
        return FALSE
