import ply.yacc as yacc
from lex import tokens


functions = {}

# Define grammar rules
def p_statement_function(p):
    '''
    statement : FUNCTION_DEFINITION
              | expression
    '''
    p[0] = p[1]

def p_function_definition(p):
    'FUNCTION_DEFINITION : COLON WORD LPAREN FUNCTION_PARAMS RPAREN FUNCTION_BODY'

    function_name = p[2]
    function_params = p[4]
    function_body = p[6]

    functions[function_name] = (function_params, function_body)
    
def p_function_params(p):
    '''FUNCTION_PARAMS : ID FUNCTION_PARAMS
                      | ID MINUS MINUS WORD
                      '''
    if len(p) == 2:
        p[0] = [p[1]] 
    elif len(p) == 5:
        p[0] = [p[1]] + [p[4]]



def p_function_body(p):
    '''FUNCTION_BODY : operator expression operator SEMICOLON'''
    p[0] = p[1] + p[2] + p[3]



def p_operator(p):
    '''operator : PLUS
                | MINUS
                | TIMES
                | DIVIDE'''
    p[0] = p[1]

# Define grammar rules
def p_expression_plus(p):
    'expression : expression expression PLUS'

    instruction = ''

    if isinstance(p[1], int):
        instruction += "pushi" + str(p[1]) + "\n"
    else:
        instruction += p[1]

    if isinstance(p[2], int):
        instruction += "pushi" + str(p[2]) + "\n"
    else:
        instruction += p[2]

    instruction += "add\n"

    p[0] = instruction


def p_expression_minus(p):
    'expression : expression expression MINUS'

    instruction = ''

    if isinstance(p[1], int):
        instruction += "pushi" + str(p[1]) + "\n"
    else:
        instruction += p[1]

    if isinstance(p[2], int):
        instruction += "pushi" + str(p[2]) + "\n"
    else:
        instruction += p[2]

    instruction += "sub\n"

    p[0] = instruction


def p_expression_times(p):
    'expression : expression expression TIMES'

    instruction = ''

    if isinstance(p[1], int):
        instruction += "pushi" + str(p[1]) + "\n"
    else:
        instruction += p[1]

    if isinstance(p[2], int):
        instruction += "pushi" + str(p[2]) + "\n"
    else:
        instruction += p[2]

    instruction += "mul\n"

    p[0] = instruction


def p_expression_divide(p):
    'expression : expression expression DIVIDE'
    if p[2] == 0:
        raise ZeroDivisionError("Division by zero!")

    instruction = ''

    if isinstance(p[1], int):
        instruction += "pushi" + str(p[1]) + "\n"
    else:
        instruction += p[1]

    if isinstance(p[2], int):
        instruction += "pushi" + str(p[2]) + "\n"
    else:
        instruction += p[2]

    instruction += "div\n"

    p[0] = instruction


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


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
    f.write("start\n")
    result = parser.parse(s)
    f.write(result + "writei\nstop")

    f.close()

except Exception as e:
    print(e)
