class KnowledgeBaseBase:
	"""
	A basic KnowledgeBase consisting of rules and facts.
	Entirely passive, does not deduce any knowledge beyond the given facts.
	"""
	def __init__(self, rules, facts):
		self.rules = rules
		self.facts = facts

	def query(self, q):
		return q in self.facts

	def derive(self):
		return self.facts
