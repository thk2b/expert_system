from knowledge_base import KnowledgeBase
from expressions import *

if __name__ == '__main__':
    kb = KnowledgeBase({
        Atom('A'): [Atom('B')],
        Atom('B'): [Atom('C')],
    }, [
        Atom('A')
    ])
    print(kb.query(Atom('C'), True))
