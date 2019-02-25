from KnowledgeBase import KnowledgeBase

if __name__ == '__main__':
    kb = KnowledgeBase({'A': 'B', 'B': 'C'}, 'A')
    kb = KnowledgeBase({'A & B': 'C', 'B1': 'B', 'C | D': 'E'}, ['A', 'B1'])
    print(kb.evaluate_atom('E'))
