from KnowledgeBase import KnowledgeBase
from expressions import *

if __name__ == '__main__':
    kb = KnowledgeBase({
        Atom('A'): [Atom('B')],
        Atom('B'): [Atom('C')],
        AndExpression(Atom('A'), Atom('C')): [Atom('D')]
    }, [
        Atom('A')
    ])
    # kb.query(Atom('C'), True)
    kb.query(Atom('D'), True)
