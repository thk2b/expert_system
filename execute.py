import sys
import parser
import graph
from pushback_iter import pushback_iter
from preprocess_iter import preprocess_iter
from node import tv_to_str

PROMPT = 'e> '

def execute_file(filename, verbose=False):
    """
    Parse a file and execute queries
        parse rules
        parse 
    """
    g = graph.Graph()
    with open(filename, 'r') as file:
        execute_sessions(g, file, False, verbose)

def execute_interactive(verbose=False):
    g = graph.Graph()
    while True:
        try:
            execute_sessions(g, sys.stdin, True, verbose)
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        except Exception as e:
            print('ERROR: ', e) #FIXME: Make sure errors don't mess up the graph

def execute_sessions(g, file, interactive=False, verbose=False):
    pb_file = pushback_iter(preprocess_iter(file, PROMPT if interactive else None))
    while True:
        try:
            execute_session(g, pb_file, verbose)
        except EOFError:
            break

def execute_session(g, file, verbose=False):
    """
    Execute a session from the file
        Read rules and add to the graph
        Read statements and close the graph
        Read and execute queries and reset the graph
    """
    parser.parse_rules(g, file)
    statements = parser.parse_statements(g, file)
    got_query = False
    with g.suppose(statements):
        for query in parser.parse_queries(g, file):
            got_query = True
            tv = tv_to_str(g.eval(query, verbose=verbose))
            if verbose:
                print("therefore {} is {}".format(query, tv))
            else:
                print("{}: {}".format(query, tv))
    if not len(statements) and not got_query:
        raise SyntaxError('Invalid statement, expected rule, {}, or {}'.format(parser.terminals['ASSERT'], parser.terminals['QUERY']))

if __name__ == '__main__':
    execute_file('a.exp')
