import graph
import node

def main():
    # g = graph.Graph()
    # e = g.entails(g.atom('A'), g.atom('B'))
    # g.entails(e, g.atom('C'))
    # print(g.eval(g.atom('C'), [g.atom('D')]))
    # # g.entails(node.And(g.atom('A'), g.atom('B')), g.atom('C'))
    # # print(g)

    g  = graph.Graph()
    g.entails(g.atom('A'), g.atom('B'))
    g.entails(g.atom('A'), g.atom('C'))
    g.entails(
        node.And(g.atom('B'), g.atom('C')),
        g.atom('D')
    )
    print(g.eval(g.atom('D'), []))

if __name__ == "__main__":
    main()
