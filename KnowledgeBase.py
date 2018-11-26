
class Rule:
	def __init__(self, antecedent, concequent):
		self.antecedent = antecedent
		self.concequent = concequent

class Facts:
	def __init__(self, expressions):
		self.expressions = expressions

	def __contains__(self, expression):
		for e in self.expressions:
			if e == expression:
				return True
		return False

class AtomicExpression:
	def __init__(self, symbol):
		self.symbol = symbol

	def __eq__(self, other):
		return isinstance(other, AtomicExpression)\
			and other.symbol == self.symbol

	def evaluate(self, facts):
		return self in facts

class BinaryExpression:
	def __init__(self, left_expr, right_expr):
		self.right_expr = right_expr
		self.left_expr = left_expr

	def __eq__(self, other):
		return isinstance(other, BinaryExpression)\
			and other.right_expr == self.right_expr\
			and other.left_expr == self.left_expr

	def evaluate(self, facts):
		return self.right_expr.evaluate(facts) and self.right_expr.evaluate(facts)

if __name__ == "__main__":
	symbols = ['A', 'B', 'Z']
	f = Facts([AtomicExpression(s) for s in symbols])
	print (repr(AtomicExpression('a') in f))
