import error
T, I, F = TRUE, INDETERMINATE, FALSE = 1, 0, -1

def bool_to_tv(b):
    return T if b else F

TV_TABLE = {I:'indeterminate', T:'true', F:'false'}

def tv_to_str(tv):
    return TV_TABLE[tv]

class Node:
    """Represents a basic node in the knowledge graph"""
    def __init__(self):
        """
        Members:
            skip: Ignore this node
        """
        self.skip = False

class Atom(Node):
    def __init__(self, name, graph, tv=INDETERMINATE):
        super().__init__()
        if not name.isalnum():
            raise SyntaxError('Invalid atom name: {}'.format(name))
        self.original_tv = tv if tv is not INDETERMINATE else None
        self.tv = tv
        self.tv_reason = None
        self.name = name
        self.graph = graph
        self.inputs = []
        self.outputs = []

    def eval(self, child=None, verbose=False):
        if self.tv != INDETERMINATE:
            if verbose:
                if self.tv_reason:
                    print("{} is {} because {}".format(self, tv_to_str(self.tv), self.tv_reason))
                else:
                    print("{} is {}".format(self, tv_to_str(self.tv)))
            return self.tv
        all_indeterminate = True
        for i in self.inputs:
            if i.skip:
                continue
            tv = i.eval(self)
            if tv != INDETERMINATE:
                all_indeterminate = False
            if tv == TRUE:
                self.tv = TRUE
                if verbose:
                    self.tv_reason = "{} is {}".format(i, tv_to_str(self.tv))
                    print("{} is {} because {}".format(
                        self, tv_to_str(self.tv), self.tv_reason))
                return TRUE
        if all_indeterminate:
            self.tv = INDETERMINATE
        else:
            self.tv = FALSE
        if verbose:
            print("{} is {}".format(self, tv_to_str(self.tv)))
        return self.tv

    def __str__(self):
        return self.name

class INot(Node):
    def __init__(self, input_node):
        super().__init__()
        if isinstance(input_node, Atom):
            input_node.outputs.append(self)
        else:
            input_node.output = self
        self.input = input_node
        self.output = None

    def eval(self, child=None, verbose=False):
        tv = self.input.eval(self)
        if tv != INDETERMINATE:
            out_tv = T if tv is F else F
            if verbose:
                print('{} is {} because {} is {}'.format(
                    self, tv_to_str(out_tv), self.input, tv_to_str(tv)))
            return out_tv
        if verbose:
            print('{} is {} because {} is {}'.format(
                self, tv_to_str(INDETERMINATE), self.input, tv_to_str(INDETERMINATE)))
        return INDETERMINATE

    def __str__(self):
        return "not({})".format(str(self.input))

class BinaryInputNode(Node):
    """
    InputNode: has 2 inputs, one output
    """
    def __init__(self, i1, i2, **kwargs):
        super().__init__(**kwargs)
        self.i1, self.i2 = i1, i2
        self.output = None

class IAnd(BinaryInputNode):
    def eval(self, child=None, verbose=False):
        for i in (self.i1, self.i2):
            if i.skip:
                continue
            tv = i.eval(self)
            if tv != TRUE:
                if verbose:
                    print('{} is {} because {} is {}'.format(
                        self, tv_to_str(FALSE), i, tv_to_str(tv)))
                return tv
        if verbose:
            print('{} is {} because {} and {} are true'.format(
                self, tv_to_str(TRUE), self.i1, self.i2))
        return TRUE

    def __str__(self):
        return "({} and {})".format(str(self.i1), str(self.i2))

class IOr(BinaryInputNode):
    """Represents an or node in the knowledge graph"""
    def eval(self, child=None, verbose=False):
        for i in (self.i1, self.i2):
            if i.skip:
                continue
            tv = i.eval(self)
            if tv == TRUE:
                if verbose:
                    print('{} is {} because {} is {}'.format(
                        self, tv_to_str(TRUE), i, tv_to_str(TRUE)))
                return TRUE
        if verbose:
            print('{} is {} because {} is {}'.format(
                self, tv_to_str(FALSE), i, tv_to_str(tv)))
        return FALSE

    def __str__(self):
        return "({} or {})".format(str(self.i1), str(self.i2))

class IXor(BinaryInputNode):
    def eval(self, child=None, verbose=False):
        tv1 = self.i1.eval() if not self.i1.skip else FALSE
        tv2 = self.i2.eval() if not self.i2.skip else FALSE
        if tv1 == INDETERMINATE or tv2 == INDETERMINATE:
            if verbose:
                print('{} is {} because {} is {}'.format(
                    self, tv_to_str(tv),
                    self.i1 if tv1 == INDETERMINATE else self.i2,
                    tv_to_str(tv)))
            return INDETERMINATE
        if tv1 == tv2:
            if verbose:
                print('{} is {} because {} and {} are {}'.format(
                    self, tv_to_str(FALSE), self.i1, self.i2, tv_to_str(tv1)))
            return FALSE
        if verbose:
            print('{} is {} because {} is {} and {} is {}'.format(
                self, tv_to_str(TRUE),
                self.i1, tv_to_str(tv1),
                self.i2, tv_to_str(tv1)))
        return TRUE

    def __str__(self):
        return "({} xor {})".format(str(self.i1), str(self.i2))

class ONot(Node):
    def __init__(self, output_node):
        super().__init__()
        if isinstance(output_node, Atom):
            output_node.inputs.append(self)
        else:
            output_node.input = self
        self.output = output_node
        self.input = None

    def eval(self, child=None, verbose=False):
        tv = self.input.eval(self)
        if tv == TRUE: #negate input only if node is true
            return FALSE
        return tv

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
    def eval(self, child, verbose=False):
        return self.input.eval(self)
    
    def __str__(self):
        return '({} and {})'.format(self.o1, self.o2)

class OOr(BinaryOutputNode):
    def eval(self, child, verbose=False):
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

    def __str__(self):
        return '({} or {})'.format(self.o1, self.o2)

class OXor(BinaryOutputNode):
    def eval(self, child, verbose=False):
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

    def __str__(self):
        return '({} or {})'.format(self.o1, self.o2)
