import node as node
import graph as graph

import collections

"""
Grammar
    Sessions            = Session Sessions
                        | EOF
    Session             = Rules Statements Queries
    Rules               = Rule Rules
                        | NULL
    Statements          = Statement Statements
                        | NULL
    Queries             = Query Queries
                        | NULL

    Rule                = Expr ENTAILS Expr
    Statement           = ASSERT AtomList
    Query               = QUERY ExprList

    Expr                = XorExpr
    XorExpr             = Expr XOR Expr
                        | OrExpr
    OrExpr              = Expr OR Expr
                        | AndExpr
    AndExpr             = Expr AND Expr
                        | AtomExpr
    NotExpr             = NOT AtomExpr
                        | AtomExpr
    AtomExpr            = LPAREN Expr RPAREN
                        | Atom
    Atom                = <NAME>

    ExprList            | Expression LIST_SEPARATOR ExprList
                        | AtomList
                        | NULL
    AtomList            = CompactAtomList
                        | SeparatedAtomList
    CompactAtomList     = <NAME(len=1)> CompactAtomList
                        | NULL
    SeparatedAtomList   = Atom LIST_SEPARATOR SeparatedAtomList
                        | NULL
"""

terminals = {
    "NEWLINE":          "\n",
    "ENTAILS":          "=>",
    "ASSERT":           "=",
    "QUERY":            "?",
    "AND":              "+",
    "OR":               "|",
    "XOR":              "^",
    "NOT":              "!",
    "LIST_SEPARATOR":   ",",
    "LPAREN":           "(",
    "RPAREN":           ")",
}

def parse_rules(g, file):
    for line in file:
        if parse_rule(g, line):
            continue
        file.push(line)
        return
    raise EOFError()

def parse_rule(g, line):
    if terminals["ENTAILS"] in line:
        l, r = map(lambda s: s.strip(), line.split(terminals["ENTAILS"]))
        if not r:
            raise SyntaxError('Expected concequent')
        g.entails(parse_expr(g, l, True), parse_expr(g, r, False))
        return True
    return None

def parse_statements(g, file):
    statements = collections.deque()
    got_valid_statement = False
    for line in file:
        statement_list = parse_statement(g, line)
        if statement_list is not None:
            got_valid_statement = True
            for statement in statement_list:
                statements.append(statement)
        else:
            file.push(line)
            return statements if got_valid_statement else []
    raise EOFError()

def parse_queries(g, file):
    for line in file:
        query = parse_query(g, line)
        if query is None:
            file.push(line)
            return
        for expr in query:
            yield expr
    raise EOFError()

def parse_statement(g, line):
    line = line.strip()
    if line[0] != terminals['ASSERT']:
        return None
    return parse_atom_list(g, line[1:])

def parse_expr_list(g, line, is_input):
    if terminals['LIST_SEPARATOR'] in line:
        return [
            parse_expr(g, expr_str, is_input)
            for expr_str in map(lambda s: s.strip(), line.split(terminals['LIST_SEPARATOR']))
            if len(expr_str)
        ]
    return [g.atom(name) for name in list(line.strip()) if name != ' '] 

def parse_atom_list(g, line):
    if terminals['LIST_SEPARATOR'] in line:
        return [
            g.atom(name.strip()) for name in line.split(terminals['LIST_SEPARATOR'])
        ]
    return [g.atom(name) for name in list(line.strip()) if name != ' ']

def parse_query(g, line):
    line = line.strip()
    if line[0] != terminals['QUERY']:
        return None
    return parse_expr_list(g, line[1:], True)

def parse_expr(g, s, is_input):
    return parse_xor_expr(g, s, is_input)

def split(s, token):
    """
    split s into two stripped strings at the first-non parenthesized occurence of c
    Returns:
        str, str or None, None if c does not occur in s outside parentheses
    """
    paren_level = 0
    for i, c in enumerate(s):
        if c == terminals['LPAREN']:
            paren_level += 1
            while s[i] != terminals['RPAREN']:
                i += 1
        elif c == terminals['RPAREN']:
            paren_level -= 1
            if paren_level < 0:
                raise SyntaxError('Unmatched RPAREN')
        elif paren_level == 0 and s[i:i+len(token)] == token:
            return s[:i].strip(), s[i+len(token):].strip()
    if paren_level != 0:
        raise SyntaxError('Unmatched LPAREN')
    return None, None

def parse_xor_expr(g, s, is_input):
    l, r = split(s, terminals["XOR"])
    if not l:
        return parse_or_expr(g, s, is_input)
    return (node.IXor if is_input else node.OXor)(parse_expr(g, l, is_input), parse_expr(g, r, is_input))

def parse_or_expr(g, s, is_input):
    l, r = split(s, terminals["OR"])
    if not l:
        return parse_and_expr(g, s, is_input)
    return (node.IOr if is_input else node.OOr)(parse_expr(g, l, is_input), parse_expr(g, r, is_input))

def parse_and_expr(g, s, is_input):
    l, r = split(s, terminals["AND"])
    if not l:
        return parse_not_expr(g, s, is_input)
    return (node.IAnd if is_input else node.OAnd)(parse_expr(g, l, is_input), parse_expr(g, r, is_input))

def parse_not_expr(g, s, is_input):
    l, r = split(s, terminals["NOT"])
    if r:
        return (node.INot if is_input else node.ONot)(parse_expr(g, r, is_input))
    return parse_atom_expr(g, s, is_input)

def parse_atom_expr(g, s, is_input):
    if s[0] == terminals['LPAREN']:
        if s[-1] != terminals['RPAREN']:
            raise SyntaxError('Unmatched LPAREN')
        return parse_expr(g, s[1:-1], is_input)
    if (len(s) == 0):
        raise SyntaxError('Empty Atom')
    a = s.split()
    if (len(a) > 1):
        raise SyntaxError('Unexpected Atom: {}'.format(a))
    if not a[0].isalnum():
        raise SyntaxError('Invalid character in Atom: {}'.format(a[0]))
    return g.atom(a[0].strip())
