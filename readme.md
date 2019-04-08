# expert system

A propositional logic engine

## Usage

```
$ ./expert_system -h
usage: expert_system [-h] [--verbose] [filename [filename ...]]

positional arguments:
  filename       file to execute (default: stdin)

optional arguments:
  -h, --help     show this help message and exit
  --verbose, -v  verbose mode-
```

Alterntively, run with `$ python3 expert_system`

Run unit tests with `$ python3 test.py`

## Examples

```
$ ./expert_system -v
e> a => b # if a then b
e> =a     # a is true
e> ?b     # what about b
b is true because a is true
e> =      # nothing is true
e> ?b
b is false
```

```
A => B + C
B => D | E
C => ! E

=A
?D # true
```

## Syntax

The parser implements the following grammar:
```
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

    Rule                = Expression ENTAILS Expression
    Statement           = ASSERT AtomList
    Query               = QUERY ExpressionList

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

    ExpressionList      | Expression LIST_SEPARATOR ExpressionList
                        | AtomList
                        | NULL
    AtomList            = CompactAtomList
                        | SeparatedAtomList
    CompactAtomList     = <NAME(len=1)> CompactAtomList
                        | NULL
    SeparatedAtomList   = Atom LIST_SEPARATOR SeparatedAtomList
                        | NULL

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

```

## Algorithm and API

A backward-chaining algorithm (with caching) is used to respond to queries.

Inputed rules are transformed into a data-flow graph, and queries are lazily-executed.
