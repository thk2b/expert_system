import sys
import parser
import graph
from pushback_iter import pushback_iter
from preprocess_iter import preprocess_iter
from node import tv_to_str

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
            execute_sessions(g, sys.stdin, True)
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        except Exception as e:
            print('ERROR: ', e) #FIXME: Make sure errors don't mess up the graph

def execute_sessions(g, file, interactive=False):
    pb_file = pushback_iter(preprocess_iter(file, PROMPT if interactive else None))
    while True:
        try:
            execute_session(g, pb_file, interactive)
        except EOFError:
            break

def execute_session(g, file, interactive=False):
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
            print("therefore {} is {}".format(query, tv_to_str(g.eval(query, verbose=interactive))))

if __name__ == '__main__':
    execute_file('a.exp')
