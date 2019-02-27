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

    def evaluate(self, expr):
        """
            Given current facts, determine expr
        returns:
            True if expr is justified by existing facts
            False otherwise
        """
        for fact in self.facts:
            if fact.determines(expr):
                return fact.entails(expr)
        return False

    def infer(self, expr):
        """
            Given rules, determine one antecedent leading to expr
        returns:
            True if a rule leading to expr was expanded
            False otherwise
        """
        for antecedent, concequents in self.rules.items():
            for concequent in concequents:
                if concequent.determines(expr) and self.query(antecedent, verbose):
                    self.facts.append(antecedent)
                    return True
        return False

    def query(self, expr, verbose=False): 
        if self.evaluate(expr):
            return True
        if self.infer(expr):
            return self.evaluate(expr)
        return False

    def query(self, expr, verbose=False):
        if expr.evaluate(self, verbose):
            if verbose:
                print("{} is True.".format(expr))
            return True
        for antecedent, concequents in self.rules.items():
            for concequent in concequents:
                if expr in concequent and self.query(antecedent, verbose):
                    # self.facts.append(antecedent)
                    if verbose:
                        print("Therefore {} is True.".format(expr))
                    # return expr.evaluate(self, verbose)
                    return True #FIXME: True antecedent entails Truth value of concequent
        return False

    def add_fact(self, expr):
        self.facts.append(expr)

    def add_rule(self, antecedent, concequent):
        self.rules[antecedent] = concequent
