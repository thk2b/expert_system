class Expression:
    pass

class Atom(Expression):
    def __init__(self, symbol):
        self.symbol = symbol

    def evaluate(self, kb, verbose=False):
        """
            Evaluate whether self is true given Facts
        """
        for fact in kb.facts:
            if isinstance(fact, Atom): # TODO: handle other types
                if fact.symbol == self.symbol:
                    return True
        return False

    def __contains__(self, expr):
        if isinstance(expr, Atom):
            return expr.symbol == self.symbol
        return False

    def __repr__(self):
        return "<Fact '{}'>".format(self.symbol)

    def __str__(self):
        return "'{}'".format(self.symbol)

class NotExpression(Expression):
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, kb, verbose=False):
        return not kb.query(self.expr)

    def __repr__(self):
        return "<NotExpression '{}'>".format(self.symbol)

    def __str__(self):
        return "!{}".format(self.expr)

class BinaryExpression(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.as_tuple = (left, right)

    def evaluate(self, kb, verbose=False):
        raise NotImplementedError('Must be implemented by subclass')

class AndExpression(BinaryExpression):
    def evaluate(self, kb, verbose=False):
        if kb.query(self.left, verbose) and kb.query(self.right, verbose):
            if verbose:
                print("Therefore {} is True".format(self))
            return True

    def __repr__(self):
        return "<AndExpression {} + {}>".format(repr(self.left), repr(self.right))

    def __str__(self):
        return "{} + {}".format(str(self.left), str(self.right))

class XorExpression(BinaryExpression):
    def evaluate(self, kb, verbose=False):
        l = kb.query(self.left, verbose)
        r = kb.query(self.right, verbose)
        return l and not r or r and not l

    def __repr__(self):
        return "<XorExpression {} + {}>".format(repr(self.left), repr(self.right))

    def __str__(self):
        return "{} ^ {}".format(self.left, self.right)

class OrExpression(BinaryExpression):
    def evaluate(self, kb, verbose=False):
        return kb.query(self.left, verbose) or kb.query(self.right, verbose)

    def __repr__(self):
        return "<OrExpression {} + {}>".format(repr(self.left), repr(self.right))

    def __str__(self):
        return "{} + {}".format(self.left, self.right)
