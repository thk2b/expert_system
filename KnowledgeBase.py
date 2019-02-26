from expressions import Atom

class KnowledgeBase:
    def __init__(self, rules={}, facts=[]):
        """
        Knowledge Base
            rules: dict of Expr(antecedent): [Expr(concequent)].
                If the antecedent is true, the concequent must be true
            facts: list of Expressions known to be true
        """
        self.rules = rules
        self.facts = facts

    def query(self, expr, verbose=False):
        if expr.evaluate(self.facts):
            return True
        for antecedent, concequents in self.rules.items():
            for concequent in concequents:
                if expr in concequent and self.query(antecedent, verbose):
                    # concequent may entail expr and antecedent is true
                    # if concequent.evaluate(expr, self.facts):
                        # facts and concequent entail expression
                    if verbose:
                        print("Therefore {} is True.".format(expr))
                    return True
        return False

    def add_fact(self, expr):
        self.facts.append(expr)

    def add_rule(self, antecedent, concequent):
        self.rules[antecedent] = concequent
