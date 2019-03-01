import node as n
import graph as g

"""
Grammar
    Session                = Rules Statements Queries Session
                        | EOF
    Rules               = Rule Rules
                        | NotRule
    Statements          = Statement Statements
                        | NotStatement
    Queries             = Query Queries
                        | NotQuery

    Line                = Rule      NEWLINE
                        | Statement NEWLINE
                        | Query     NEWLINE

    Rule                = Expression ENTAILS Expression
    Statement           = ASSERT AtomList
    Query               = QUERY ExpressionList

    Expr                = NotExpr
    NotExpr             = NOT Expr
                        | OrExpr
    OrExpr              = Expr OR Expr
                        | AndExpr
    AndExpr             = Expr AND Expr
                        | AtomExpr
    AtomExpr            = LPAREN Expr RPAREN
                        | Atom
    Atom                = <NAME>

    ExpressionList      = Expression
                        | Expression LIST_SEPARATOR ExpressionList
                        | NULL
    AtomList            = CompactAtomList
                        | SeparatedAtomList
    CompactAtomList     = <NAME(len=1)> CompactAtomList
                        | NULL
    SeparatedAtomList   = Atom LIST_SEPARATOR SeparatedAtomList
                        | NULL

The following terminals must be defined
    NEWLINE         \n
    ENTAILS         ->
    ASSERT          =
    QUERY           ?
    AND             +
    OR              |
    XOR             ^
    NOT             !
    LIST_SEPARATOR  ,
"""

def execute_file(filename):
    """
    Parse a file and execute queries
        parse rules
        parse 
    """
    pass

def execute_interactive():
    pass

def parse_line(graph, line):
    """Parse a line of input and update the graph"""
    pass

def parse_rule(graph, line):
    """Parse a rule and add call graph.entails"""
    pass

def parse_statement(graph, line):
    """Parse statement facts and close the graph"""
    pass

def parse_query(graph, line):
    """Parse query and print the result"""
    pass

def parse_expr(graph, s):
    pass

def parse_not_expr(graph, s):
    pass

def parse_xor_expr(graph, s):
    pass

def parse_or_expr(graph, s):
    pass

def parse_and_expr(graph, s):
    pass

def parse_atom_expr(graph, s):
    pass
