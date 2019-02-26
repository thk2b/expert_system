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

    def evaluate(self):
        # FIXME: evaluate belongs to KnowledgeBase, not expressions?
        pass

    def query(self, expr, verbose=False):
        if expr.evaluate(self, verbose):
            if verbose:
                print("{} is True.".format(expr))
            return True
        for antecedent, concequents in self.rules.items():
            for concequent in concequents:
                if expr in concequent and self.query(antecedent, verbose):
                    if verbose:
                        print("Therefore {} is True.".format(expr))
                    # return expr.evaluate(self, verbose)
                    return True #FIXME: True antecedent entails Truth value of concequent
        return False

    def add_fact(self, expr):
        self.facts.append(expr)

    def add_rule(self, antecedent, concequent):
        self.rules[antecedent] = concequent
