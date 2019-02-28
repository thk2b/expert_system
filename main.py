from graph import *
from node import *
from error import *

#Example input: 
# B => A 
# D + E => B 
# G + H => F 
# I + J => G 
# G => H 
# L + M => K 
# O + P => L + N 
# N => M 

# [INITIAL FACTS HERE] 
# ?AFKP 

# With =DEIJOP, AFKP is true. 
# With =DEIJP, AFP is true, K is false. 
def main():
    g = Graph()
    g.entails(g.atom('B'), g.atom('A'))
    g.entails(IAnd(g.atom('D'), g.atom('E')), g.atom('B'))
    g.entails(IAnd(g.atom('G'), g.atom('H')), g.atom('F'))
    g.entails(IAnd(g.atom('I'), g.atom('J')), g.atom('G'))
    g.entails(g.atom('G'), g.atom('H'))
    g.entails(IAnd(g.atom('L'), g.atom('M')), g.atom('K'))
    g.entails(IAnd(g.atom('O', tv=FALSE), g.atom('P')), OAnd(g.atom('L'), g.atom('N')))
    g.entails(g.atom('N'), g.atom('M'))

    print(g.eval(g.atom('A'), [
        g.atom('D'),
        g.atom('E'),
        g.atom('I'),
        g.atom('J'),
        g.atom('O'),
        g.atom('P'),
    ]))
    print(g.eval(g.atom('F')))
    print(g.eval(g.atom('P')))
    print(g.eval(g.atom('K')))

if __name__ == "__main__":
    main()
