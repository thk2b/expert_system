class Expression:
    pass

class Atom(Expression):
    def __init__(self, symbol):
        self.symbol = symbol

    def determines(self, expr, kb):
        """
        Returns True if the truth value of self determines the truth value of expr,
            with respect to the facts of kb, False otherwise
        """
        if isinstance(expr, Atom):
            return expr.symbol == self.symbol
        if isinstance(expr, NotExpression):
            return self.determines(expr.expr, kb)
        if isinstance(expr, AndExpression):
            determines_left = self.determines(expr.left, kb)
            determines_right = self.determines(expr.right, kb)
            if determines_left and determines_left:
                return True
            if determines_left: # return True only if self entirely determines expr. Consider throwing IntedetminateError
                return kb.query(expr.right)
            else: #determines_right
                return kb.query(expr.left)
        if isinstance(expr, OrExpression):
            return self.determines(expr.left, kb) or self.determines(expr.right, kb)
        if isinstance(expr, XorExpression):
            determines_left = self.determines(expr.left, kb)
            determines_right = self.determines(expr.right, kb)
            if determines_left and determines_right:
                return False
            return determines_left or determines_right

    def entails(self, expr, kb):
        """
        Returns True if self being true entails that expr is True,
            with respect to the facts of kb, False otherwise
        self must determine expr
        """
        if isinstance(expr, Atom):
            return expr.symbol == self.symbol
        if isinstance(expr, NotExpression):
            return not self.entails(expr.expr, kb)
        if isinstance(expr, AndExpression):
            entails_left = self.entails(expr.left, kb)
            entails_right = self.entails(expr.right, kb)
            if entails_left and entails_left:
                return True
            if entails_left: # return True only if self entirely determines expr. Consider throwing IntedetminateError
                return kb.query(expr.right)
            else: #entails_right
                return kb.query(expr.left)
        if isinstance(expr, OrExpression):
            return self.entails(expr.left, kb) or self.entails(expr.right, kb)
        if isinstance(expr, XorExpression):
            entails_left = self.entails(expr.left, kb)
            entails_right = self.entails(expr.right, kb)
            if entails_left and entails_right:
                return False
            return entails_left or entails_right

    def __repr__(self):
        return "<Fact '{}'>".format(self.symbol)

    def __str__(self):
        return "'{}'".format(self.symbol)

class NotExpression(Expression):
    def __init__(self, expr):
        self.expr = expr

    def determines(self, expr, kb):
        if isinstance(expr, Atom):
            return self.expr.determines(expr, kb)
        if isinstance(expr, NotExpression):
            return self.expr.determines(expr.expr, kb)
        if isinstance(expr, AndExpression):
            determines_left = self.expr.determines(expr.left, kb)
            determines_right = self.expr.determines(expr.right, kb)
            if determines_left and determines_left:
                return True
            if determines_left: # return True only if self entirely determines expr. Consider throwing IntedetminateError
                return kb.query(expr.right)
            else: #determines_right
                return kb.query(expr.left)
        if isinstance(expr, OrExpression):
            return self.expr.determines(expr.left, kb) or self.expr.determines(expr.right, kb)
        if isinstance(expr, XorExpression):
            determines_left = self.expr.determines(expr.left, kb)
            determines_right = self.expr.determines(expr.right, kb)
            if determines_left and determines_right:
                return False
            return determines_left or determines_right

    def entails(self, expr, kb):
        if isinstance(expr, Atom):
            return not self.expr.entails(expr, kb)
        if isinstance(expr, NotExpression):
            return not self.expr.entails(expr, kb)
        if isinstance(expr, AndExpression):
            entails_left = self.expr.entails(expr.left, kb)
            entails_right = self.expr.entails(expr.right, kb)
            if entails_left and entails_left:
                return True
            if entails_left:
                return kb.query(expr.right)
            else:
                return kb.query(expr.left)
        if isinstance(expr, OrExpression):
            return self.expr.entails(expr.left, kb) or self.expr.entails(expr.right, kb)
        if isinstance(expr, XorExpression):
            entails_left = self.expr.entails(expr.left, kb)
            entails_right = self.expr.entails(expr.right, kb)
            if entails_left and entails_right:
                return False
            return entails_left or entails_right

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
    def evaluate(self, kb, verbose=False): # TODO: remove verbose
        if kb.query(self.left, verbose) and kb.query(self.right, verbose):
            # if verbose:
                # print("Therefore {} is True".format(self))
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
