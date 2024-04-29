import ply.lex as lex

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'COLON',
    'SEMICOLON',
    'WORD',
    'ID',
)

t_RPAREN = r'\)'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_PLUS = r'\+'
t_COLON = r':'
t_SEMICOLON = r';'

parameter_list = False

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_WORD(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    global parameter_list
    if parameter_list or t.value == '(':
        t.type = 'ID'
    return t

def t_ID(t):
    r'[a-z]'
    global parameter_list
    if t.value == '-':
        t.type = 'WORD'
    return t

def t_LPAREN(t):
    r'\('
    global parameter_list
    parameter_list = True
    return t

def t_MINUS(t):
    r'\-'
    global parameter_list
    parameter_list = False
    return t

t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# def lexer_debug(example):
#     lexer.input(example)
#     while token := lexer.token():
#         print(token)

# exemplo = ": AVERAGE ( a b -- avg ) + 2/ ;"
# lexer_debug(exemplo)
