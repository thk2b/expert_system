import error
T, I, F = TRUE, INDETERMINATE, FALSE = 1, 0, -1

def bool_to_tv(b):
    return T if b else F

TV_TABLE = {I:'I', T:'T', F:'F'}

class Node:
    """Represents a basic node in the knowledge graph"""
    def __init__(self, tv=INDETERMINATE):
        """
        Args:
        """
        self.tv = tv
        self.skip = False

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

class Atom(Node):
    def __init__(self, name, graph, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
            if i.eval(self) != INDETERMINATE:
                self.tv = i.tv
                return self.tv
        return INDETERMINATE
        # raise error.IndeterminateException("{} recieved only indeterminate inputs".format(str(self)))

    def __str__(self):
        return "Atom({})[{}]".format(self.name, TV_TABLE[self.tv])

class INot(Node):
    """Represents a not node in the knowledge graph"""
    def __init__(self, input_node):
        super().__init__()
        input_node.outputs.append(self)
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
            self.tv = T if tv is F else F
            return self.tv
        raise error.IndeterminateException("Not reived an indeterminate input")

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
        """
        Evaluate the truth value of this node
            if node is not indeterminate return self.tv
            all(
                for each node in self.input if node is not indeterminate return node.tv
            )
        """
        for i in (self.i1, self.i2):
            if i.skip:
                continue
            if i.eval(self) == INDETERMINATE:
                raise error.IndeterminateException("And reived an indeterminate inputs")
            if i.tv == FALSE:
                self.tv = FALSE
                return FALSE
        self.tv = TRUE
        return TRUE

class IOr(BinaryInputNode):
    """Represents an or node in the knowledge graph"""
    def eval(self, child=None):
        """
        Evaluate the truth value of this node
            if node is not indeterminate return self.tv
            any(
                for each node in self.input if node is not indeterminate return node.tv
            )
        """
        for i in (self.i1, self.i2):
            if i.skip:
                continue
            if i.eval(self) != INDETERMINATE:
                if i.tv == TRUE:
                    self.tv = TRUE
                    return TRUE
            self.tv = i.tv
        if self.tv == INDETERMINATE:
            raise error.IndeterminateException("Or reived only indeterminate inputs")
        return FALSE

class ONot(Node):
    """Represents a not node in the knowledge graph"""
    def __init__(self, input_node):
        super().__init__()
        input_node.inputs.append(self)
        self.output = input_node
        self.input = None

    def eval(self, child=None):
        """
        Evaluate the truth value of this node
            if node is not indeterminate return self.tv
            for each node in self.input if node is not indeterminate return not node.tv
        """
        tv = self.input.eval(self)
        if tv != INDETERMINATE:
            self.tv = T if tv is F else F
            return self.tv
        raise error.IndeterminateException("Not reived an indeterminate input")

class BinaryOutputNode(Node):
    """
    OutputNode: has 2 outputs, one input
    """
    def __init__(self, o1, o2, **kwargs):
        super().__init__(**kwargs)
        self.o1, self.o2 = o1, o2
        o1.inputs.append(self)
        o2.inputs.append(self)
        self.input = None

class OAnd(BinaryOutputNode):
    def eval(self, child):
        self.tv = self.input.eval(self)
        return self.tv

class OOr(BinaryOutputNode):
    def eval(self, child):
        if (child is not self.o1) and (child is not self.o2):
            raise ValueError("Child {} is not an output node".format(child))
        if child is None:
            return INDETERMINATE
        self.tv = self.input.eval(self)
        if self.tv != TRUE:
            return self.tv
        other = self.o1 if child is self.o2 else self.o2
        self.skip = True
        other_tv = other.eval(None)
        self.skip = False
        if other_tv == FALSE:
            return TRUE
        return INDETERMINATE
