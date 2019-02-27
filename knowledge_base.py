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

    def evaluate(self, expr, verbose=False):
        """
            Given current facts, determine expr
        returns:
            True if expr is justified by existing facts
            False otherwise
        """
        for fact in self.facts:
            if fact.determines(expr, self):
                return fact.entails(expr, self)
        return False

    def infer(self, expr, verbose=False):
        """
            Given rules, determine one antecedent leading to expr
        returns:
            True if a rule leading to expr was expanded
            False otherwise
        """
        for antecedent, concequents in self.rules.items():
            for concequent in concequents:
                if concequent.determines(expr, self) and self.query(antecedent, verbose):
                    self.facts.append(concequent)
                    return True
        return False

    def query(self, expr, verbose=False): 
        if self.evaluate(expr, verbose):
            return True
        if self.infer(expr, verbose):
            return self.evaluate(expr, verbose)
        return False

    def add_fact(self, expr):
        self.facts.append(expr)

    def add_rule(self, antecedent, concequent):
        self.rules[antecedent] = concequent
