class Rule:
	def __init__(self, antecedent, concequent):
		self.antecedent = antecedent
		self.concequent = concequent

class BasicKnowledgeBase:
	def __init__(self, rules, facts):
		self.rules = rules
		self.facts = facts

	def query(self, q):
		if q in self.facts:
			return True
		for rule in self.rules:
			if rule.concequent == q:
				if self.query(rule.antecedent):
					# print(rule.antecedent + " is True so " + q + " is True")
					self.facts.add(rule.concequent)
					return True
		return False

	def derive(self):
		added = True
		while added:
			new_facts = set(self.facts)
			added = False
			for fact in self.facts:
				for rule in self.rules:
					if rule.antecedent == fact and rule.concequent not in new_facts:
						new_facts.add(rule.concequent)
						added = True
			self.facts = new_facts
	
	def __repr__(self):
		return "Facts: " + repr(sorted(self.facts))


if __name__ == '__main__':
	facts = {'B'}
	rules = [Rule('A', 'B'), Rule('A', 'Z'), Rule('B', 'C'), Rule('C', 'Z'), Rule('C', 'D'), Rule('D', 'E')]
	kb = BasicKnowledgeBase(rules, facts)
	goals = ['E', 'F']
	kb.derive()
	print(repr(kb))
	# for goal in goals:
		# print(goal + ' ' + repr(kb.query(goal)))
