# expert system

## specification

Knowledge Base:
	A set of Facts
	A set of Rules

Fact:
	An Expresion known to be True. Or and Xor expressions cannot be facts.

Rule:
	An antecedent Expression that, if True, entails a concequent Expression. Or and Xor expressions cannot be concequents.

Expression:
	An AtomicExpression or a Not or a BinaryExpression

BinaryExpression:
	Two expressions joined by an operator with a precedence
	Its truth value is some combination of the truth value of the two expressions

## algorithm

Backward Chaining

query Expression:
	if Expression is true based on facts
		return True
	for each rule
		if rule entails Expression
			if query antecedent
				add antecedent to facts
				return True
	return False
