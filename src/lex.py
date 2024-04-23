import ply.lex as lex

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

# Define token regular expressions
t_LPAREN = r'\('
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_PLUS = r'\+'
t_MINUS = r'-'
t_RPAREN = r'\)'


# Define token rules
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Ignore whitespace characters
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
