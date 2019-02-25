class Atom:
    def __init__(self, symbol):
        self.symbol = symbol
    def evaluate(self, atoms):
        return self.symbol in atoms

class BinaryExpression:
    def __init__(self, right, left):
        self.left = left
        self.right = right
        self.as_tuple = (left, right)
    def evaluate(self, atoms):
        raise NotImplementedError('Must be implemented by subclass')

class AndExpression(BinaryExpression):
    def evaluate(self, atoms):
        return self.left.evaluate(atoms) and self.right.evaluate(atoms)

class OrExpression(BinaryExpression):
    def evaluate(self, atoms):
        return self.left.evaluate(atoms) or self.right.evaluate(atoms)

# TODO: Unit test
if __name__ == '__main__':
    # e1 = OrExpression(Atom('a'), Atom('b'))
    e2 = AndExpression(OrExpression(Atom('a1'), Atom('a2')), Atom('b'))
    # print(e2.evaluate(['b', 'a2']))
