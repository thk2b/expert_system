from BasicKnowledgeBase import BasicKnowledgeBase
class Rule:
	def __init__(self, antecedent, concequent):
		self.antecedent = antecedent
		self.concequent = concequent

if __name__ == '__main__':
	facts = {'A'}
	rules = [Rule('A', 'B'), Rule('A', 'Z'), Rule('B', 'C')]
	kb = BasicKnowledgeBase(rules, facts)
	goals = ['E', 'F']
	kb.derive()
	print(repr(kb))
	# for goal in goals:
		# print(goal + ' ' + repr(kb.query(goal)))
