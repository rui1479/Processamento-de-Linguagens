import ply.yacc as yacc
from lex import tokens, lexer, count_id

"""
statement : instructions

instructions : instructions instruction
             | instruction
             | FUNCTION_DEFINITION

instruction : NUMBER
            | operator
            | PRINT
            
'FUNCTION_DEFINITION : COLON WORD LPAREN FUNCTION_PARAMS RPAREN FUNCTION_BODY SEMICOLON'

'FUNCTION_PARAMS' : FUNCTION_PARAMS PARAMS 
                    | PARAMS MIDFUNC WORD
                    
'PARAMS' : ID 
                    
FUNCTION_BODY : instructions instruction
             | instruction


PRINT : INT DOT
     | DOT QUOTE PRINT_S QUOTE
     | EMIT

operator : '+'
      | '-'
      | '*' 
      | '/'
      
"""

functions = {}


# Define grammar rules
def p_statement_function(p):
    '''
    statement : instructions
    '''

    p[0] = p[1]


def p_instructions1(p):
    '''instructions : instructions instruction operator
    '''

    instruction = ''

    if isinstance(p[1], int):
        instruction += "pushi " + str(p[1]) + "\n"
    else:
        instruction += p[1]

    if isinstance(p[2], int):
        instruction += "pushi " + str(p[2]) + "\n"
    else:
        instruction += p[2]

    if p[3] == '+':
        instruction += "add\n"
    elif p[3] == '-':
        instruction += "sub\n"
    elif p[3] == '*':
        instruction += "mul\n"
    elif p[3] == '/':
        if p[2] == 0:
            raise ZeroDivisionError("Division by zero!")
        instruction += "div\n"

    p[0] = instruction


def p_instructions2(p):
    '''instructions : instruction
    '''
    p[0] = p[1]


def p_instructions3(p):
    'instructions : FUNCTION_DEFINITION'
    p[0] = p[1]


def p_instruction_number(p):
    'instruction : NUMBER'
    p[0] = p[1]


def p_instruction_operator(p):
    'instruction : operator'
    p[0] = p[1]


def p_operator(p):
    '''operator : PLUS
                | MINUS
                | TIMES
                | DIVIDE'''
    p[0] = p[1]


def p_instruction_print(p):
    'instruction : PRINT'
    p[0] = p[1]


def p_print_num(p):
    'PRINT : NUMBER DOT'
    p[0] = "pushi" + str(p[1]) + "\nwritei\n"


def p_print_string(p):
    'PRINT : DOT QUOTE WORD QUOTE'
    p[0] = "pushs " + p[3] + "\nwrites\n"


def p_print_emit(p):
    'PRINT : EMIT'
    p[0] = "pushi 10\nputc\n"


def p_function_definition(p):
    'FUNCTION_DEFINITION : COLON WORD LPAREN FUNCTION_PARAMS RPAREN FUNCTION_BODY SEMICOLON'

    function_name = p[2]
    function_params = p[4]
    instructions = p[6]
    
    print(p[2])
    print(p[4])
    print(p[6])

    functions[function_name] = (function_params, instructions)


def p_function_params1(p):
    'FUNCTION_PARAMS : PARAMS FUNCTION_PARAMS '

    params_list = [p[1]] + p[2]

    p[0] = params_list


def p_function_params2(p):
    'FUNCTION_PARAMS : PARAMS MIDFUNC WORD'
    params_list = [p[1], p[2], p[3]]

    p[0] = params_list


def p_params_id(p):
    'PARAMS : ID'
    p[0] = p[1]


def p_params_midfunc(p):
    'PARAMS : MIDFUNC'
    p[0] = p[1]


def p_params_word(p):
    'PARAMS : WORD'
    p[0] = p[1]

def p_function_body1(p):
    'FUNCTION_BODY : instruction instructions instruction'
    
    params_list = [str(p[1]), str(p[2]), p[3]]

    p[0] = params_list
    
def p_function_body2(p):
    'FUNCTION_BODY : instruction'
    params_list = [p[1]]

    p[0] = params_list
    
def p_error(p):
    if p:
        raise SyntaxError("Syntax error at '%s'" % p.value)
    else:
        raise SyntaxError("Syntax error at EOF")


# Build the parser
parser = yacc.yacc()

f = open("result.txt", "w")
try:
    s = input('calc > ')
    lexer.input(s)
    tokens = [token for token in lexer]
    id_count = count_id(tokens)
    if id_count > 0:
        f.write("pushi 0\n" * id_count)
    f.write("start\n")
    result = parser.parse(s)
    f.write(result + "stop")

    f.close()

except Exception as e:
    print(e)
