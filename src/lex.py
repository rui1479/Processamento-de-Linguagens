import ply.lex as lex

count = 0

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
    'DOT',
    'MIDFUNC',
    'QUOTE',
    'EMIT'
)

t_RPAREN = r'\)'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_PLUS = r'\+'
t_COLON = r':'
t_SEMICOLON = r';'
t_DOT = r'\.'
t_MINUS = r'\-'
t_QUOTE = r'\"'

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

def t_MIDFUNC(t):
    r'\-{2}'
    global parameter_list
    parameter_list = False
    return t

def t_EMIT(t):
    r'EMIT'
    return t


t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def count_id(tokens):
    count = 0
    for token in tokens:
        if token.type == 'ID':
            count += 1
    return count

lexer = lex.lex()

# def lexer_debug(example):
#     lexer.input(example)
#     tokens = []
#     while token := lexer.token():
#         print(token)
#         tokens.append(token)
#     print(count_id(tokens))

# exemplo = ": AVERAGE ( a b -- avg ) + 2/ ;"
# lexer_debug(exemplo)
