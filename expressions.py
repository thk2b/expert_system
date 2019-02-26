class Expression:
    pass

class Atom(Expression):
    def __init__(self, symbol):
        self.symbol = symbol

    def evaluate(self, facts):
        for fact in facts:
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
    def evaluate(self, facts):
        return not self.expr.evaluate(facts)

class BinaryExpression(Expression):
    def __init__(self, right, left):
        self.left = left
        self.right = right
        self.as_tuple = (left, right)

    def evaluate(self, atoms):
        raise NotImplementedError('Must be implemented by subclass')

class AndExpression(BinaryExpression):
    def evaluate(self, atoms):
        # return kb.query(self.right) and kb.query(self.left)
        return self.left.evaluate(atoms) and self.right.evaluate(atoms)

class OrExpression(BinaryExpression):
    def evaluate(self, atoms):
        return self.left.evaluate(atoms) or self.right.evaluate(atoms)
