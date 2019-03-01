from graph import *
from node import *
from error import *

def main():
    g = Graph()
    g.entails(g.atom('A'), g.atom('B'))
    with g.suppose([g.atom('A')]):
        print(g.eval(g.atom('B')))

if __name__ == "__main__":
    main()
