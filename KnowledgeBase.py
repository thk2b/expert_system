from KnowledgeBaseBase import KnowledgeBaseBase

#Expressions

class Expression:
	def __init__(self, e):
		self.symbols = [e]

	def evaluate(self, facts):
		return self.symbols[0] in facts

	def __eq__(self, other):
		return isinstance(other, Expression) and self.symbols[0] == other.symbols[0]
	
	def __repr__(self):
		return self.symbols[0]

class Not(Expression):
	def __init__(self, e):
		super(Not, self).__init__(e)
	
	def evaluate(self, facts):
		return self.symbols[0] not in facts

	def __repr__(self):
		return "!" + self.symbols[0]
	

class BinaryExpression(Expression):
	def __init__(self, l, r):
		self.symbols = [l, r]

	def __eq__(self, other):
		return isinstance(other, BinaryExpression) and self.l == other.l and self.r == other.r

	def __repr__(self):
		return self.symbols[0] + " " + self.symbols[1]

class And(BinaryExpression):
	def __init__(self, l, r):
		super(And, self).__init__(l, r)

	def evaluate(self, facts):
		return self.symbols[0].evaluate(facts) and self.symbols[1].evaluate(facts)

	def __repr__(self):
		return self.symbols[0] + " & " + self.symbols[1]

class Or(BinaryExpression):
	def __init__(self, l, r):
		super(Or, self).__init__(l, r)

	def evaluate(self, facts):
		return self.symbols[0].evaluate(facts) or self.symbols[1].evaluate(facts)

	def __repr__(self):
		return self.symbols[0] + " || " + self.symbols[1]

class Xor(BinaryExpression):
	def __init__(self, l, r):
		super(Xor, self).__init__(l, r)

	def evaluate(self, facts):
		both = self.symbols[0].evaluate(facts) and self.symbols[1].evaluate(facts)
		either = self.symbols[0].evaluate(facts) or self.symbols[1].evaluate(facts)
		return either and not both

	def __repr__(self):
		return self.l + " xor " + self.r

#Rule

class Rule:
	def __init__(self, antecedent, concequent):
		self.antecedent = antecedent
		self.concequent = concequent

#KnowledgeBase

class KnowledgeBase:
	def __init__(self, rules, facts):
		self.rules = rules
		self.facts = facts

	def query(self, q):
		if q.evaluate(self.facts):
			return True
		for rule in self.rules:
			if rule.concequent == q:
				if self.query(rule.antecedent):
					self.facts.extend(rule.concequent.symbols)
					return True
		return False
	
	def derive(self):
		pass

if __name__ == "__main__":
	facts = ['C', 'D', 'Z']
	rules = [
		# Rule(
		# 	Or(
		# 		And(Expression('A'), Expression('B')),
		# 		And(Expression('C'), Expression('D'))
		# 	),
		# 	Expression('E')
		# ),
		# Rule(Expression("E"), Expression("F")),
		# Rule(And(Expression("F"), Expression("F")), Expression("G")),
		# Rule(Or(Expression('X'), Expression('Y')), Expression('Z'))
		Rule(Xor(Expression("C"), Expression("D")), Expression('E')),
		Rule(Expression("E"), Expression("G")),
		# Rule(Expression("C"), Expression("D"))
		# Rule(And(Expression('A'), Not('B')), Expression('C')),
		# Rule(Xor(Expression('A'), Expression('B')), Expression('D')),
		# Rule(Not(Expression('D')), Expression('X'))
		# Rule(And(Expression("A"), Not("B")), Expression("C")),
		# Rule(Expression("A"), And(Expression("B"), Expression("C")))
	]
	kb = KnowledgeBase(rules, facts)
	goals = [Expression("G"), Expression("D")]
	for goal in goals:
		print(repr(goal) + " is " + repr(kb.query(goal)))
	print(repr(kb.facts))
