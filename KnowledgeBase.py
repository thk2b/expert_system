class KnowledgeBase:
    def __init__(self, rules={}, facts=[]):
        """
        Knowledge Base
            rules: dict of Expr(antecedent): Expr(concequent).
                If the antecedent is true, the concequent must be true
            facts: list of Expression
        """
        self.rules = rules
        self.facts = facts

    def query(self, expr):
        for antecedent, concequent in self.rules.items():
            if expr in concequent and self.query(antecedent):
                # concequent may entail expr and antecedent is true
                if concequent.evaluate(expr, self.facts):
                    # facts and concequent entail expression
                    return True
        return False

