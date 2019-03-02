import sys
import parser
import graph
from pushback_iter import pushback_iter
from preprocess_iter import preprocess_iter

PROMPT = 'e> '

def execute_file(filename):
    """
    Parse a file and execute queries
        parse rules
        parse 
    """
    g = graph.Graph()
    with open(filename, 'r') as file:
        execute_sessions(g, file)

def execute_interactive():
    g = graph.Graph()
    while True:
        try:
            execute_sessions(g, sys.stdin, PROMPT)
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        except Exception as e:
            print('ERROR: ', e)

def execute_sessions(g, file, prompt=None):
    pb_file = pushback_iter(preprocess_iter(file, prompt))
    while True:
        try:
            execute_session(g, pb_file)
        except EOFError:
            break

def execute_session(g, file):
    """
    Read rules and add to the graph
    Read statements and close the graph
    Execute queries and reset the graph
    Execute a session from the file
    """
    parser.parse_rules(g, file)
    statements = parser.parse_statements(g, file)
    if statements is None:
        raise SyntaxError('Invalid statement, expected rule or {}'.format(parser.terminals['ASSERT']))
    got_query = False
    with g.suppose(statements):
        for query in parser.parse_queries(g, file):
            got_query = True
            print("{}: {}".format(query, g.eval(query)))

if __name__ == '__main__':
    execute_file('a.exp')
