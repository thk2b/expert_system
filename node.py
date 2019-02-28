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
            input is a set of references to dependency nodes:
                this node's truth value depends on their truth value
            output is a set of references to dependent nodes:
                their truth value depends on this node's truth value
        """
        self.inputs = []
        self.outputs = []
        self.tv = INDETERMINATE

class Atom(Node):
    def __init__(self, name, graph, *args, **kwargs):
        super().__init__()
        self.name = name
        self.graph = graph
        pass

    def eval(self):
        if self.tv != INDETERMINATE:
            return self.tv
        for i in self.inputs:
            if i.eval() != INDETERMINATE:
                self.tv = i.tv
                return self.tv
        raise error.IndeterminateException("Atom recieved only indeterminate inputs")

    def __str__(self):
        return "Atom({})[{}]".format(self.name, TV_TABLE[self.tv])

class ComposedNode(Node):
    def __init__(self, *inputs, **kwargs):
        super().__init__()
        self.inputs = list(inputs)
        for i in inputs:
            i.outputs.append(self)

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

class Not(Node):
    """Represents a not node in the knowledge graph"""
    def __init__(self, input_node):
        super().__init__()
        self.inputs[0] = input_node

    def eval(self):
        """
        Evaluate the truth value of this node
            if node is not indeterminate return self.tv
            for each node in self.input if node is not indeterminate return not node.tv
        """
        tv = self.inputs[0].eval()
        if tv != INDETERMINATE:
            self.tv = not tv
            return self.tv
        raise error.IndeterminateException("Not reived an indeterminate input")

class And(ComposedNode):
    """Represents an and node in the knowledge graph"""
    def eval(self):
        """
        Evaluate the truth value of this node
            if node is not indeterminate return self.tv
            all(
                for each node in self.input if node is not indeterminate return node.tv
            )
        """
        # self.tv = bool_to_tv(all((i.eval() == T for i in self.inputs)))
        # return self.tv
        for i in self.inputs:
            if i.eval() == INDETERMINATE:
                raise error.IndeterminateException("And reived an indeterminate inputs")
            if i.tv == FALSE:
                self.tv = FALSE
                return FALSE
        self.tv = TRUE
        return TRUE

class Or(Node):
    """Represents an or node in the knowledge graph"""
    def eval(self):
        """
        Evaluate the truth value of this node
            if node is not indeterminate return self.tv
            any(
                for each node in self.input if node is not indeterminate return node.tv
            )
        """
        # self.tv = bool_to_tv(any(i.eval() == T for i in self.inputs))
        # return self.tv
        for i in self.inputs:
            if i.eval() != INDETERMINATE:
                if i.tv == TRUE:
                    self.tv = TRUE
                    return TRUE
            self.tv = i.tv
        if self.tv == INDETERMINATE:
            raise error.IndeterminateException("Or reived only indeterminate inputs")
        return FALSE
