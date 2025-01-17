import ply.yacc as yacc
from lex import tokens, lexer, count_id, count_number

"""
statement : instructions

instructions : instructions instruction
             | instruction
             | instructions instruction WORD
             | FUNCTION_DEFINITION
             | FUNCCALL
             | WORD instructions


instruction : NUMBER
            | operator
            | PRINT
            | CARACTER
            
CARACTER : CR
        | KEY
                        
'FUNCTION_DEFINITION : COLON WORD LPAREN FUNCTION_PARAMS RPAREN FUNCTION_BODY SEMICOLON'
                     | COLON WORD PRINTFUNC SEMICOLON
                     | CONDICIONAL

FUNCTION_PARAMS : PARAMS FUNCTION_PARAMS
                | PARAMS MIDFUNC WORD
                | ID
                
FUNCTION_BODY : instructions
                | instruction
                                
                       
CONDICIONAL : instruction IF instruction ELSE instruction THEN

PRINTFUNC : DOT QUOTE words QUOTE

words : words WORD
        | WORD
        | words WORD sinais


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
      | '='
      | '<'
      | '>'
"""

functions = {}
flagN = False
flagW = False

# Define grammar rules
def p_statement_function(p):
    '''
    statement : instructions
    '''

    p[0] = p[1]


def p_instructions1(p):
    '''instructions : instructions instruction 
    '''
    instruction = ''
        
    if isinstance(p[1], int):
        instruction += "pushi " + str(p[1]) + "\n"
    else:
        instruction += p[1]

    if isinstance(p[2], str):
        if p[2] == '+':
            instruction += "add\n"
        elif p[2] == '-':
            instruction += "sub\n"
        elif p[2] == '*':
            instruction += "mul\n"
        elif p[2] == '%':
            if p[1] == 0:
                raise ZeroDivisionError("Division by zero!")
            instruction += "mod\n"
        elif p[2] == '/':
            if p[1] == 0:
                raise ZeroDivisionError("Division by zero!")
            instruction += "div\n"
        else:
            if isinstance(p[2], int):
                instruction += "pushi " + str(p[2]) + "\n"
            
        if p[2] == '.':
            instruction += "writei\n"

    else:
        instruction += "pushi " + str(p[2]) + "\n"

    p[0] = instruction


def p_instructions2(p):
    '''instructions : instruction
    '''
    p[0] = p[1]


def p_instructions3(p):
    '''instructions : instructions instruction WORD
    '''
    instruction = ''
    function_name = p[3]
    function_info = functions[function_name] 
    
    if "if" in function_info and "else" in function_info and "then" in function_info:
        operador = function_info['opera']
        primparam = function_info['primeiro']
        segundparam = function_info['segundo']
        
        if operador == '<':
            operador = 'inf'
        elif operador == '>':
            operador = 'sup'
        elif operador == '=':
            operador = 'equals'
        
        instruction = 'start\npushi ' + str(p[1])+ '\npushi ' + str(p[2])+ '\n' + operador + '\njz ELSE0\njump ELSE2\nELSE0:\npushs ' + primparam + '\njump ENDIF\nELSE2:\npushs ' + segundparam + '\njump ENDIF\nENDIF:\nstop\n'

        p[0] = instruction
        return
    else:
        x = count_number(tokens)

        if isinstance(p[2], int):
            instruction += "pushi " + str(p[2]) + "\n"
        else:
            instruction += p[2]

        if p[1] == '+':
            instruction += "add\n"
        elif p[1] == '-':
            instruction += "sub\n"
        elif p[1] == '*':
            instruction += "mul\n"
        elif p[1] == '=':
            instruction += "eq\n"
        elif p[1] == '<':
            instruction += "inf\n"
        elif p[1] == '>':
            instruction += "sup\n"
        elif p[1] == '%':
            if p[2] == 0:
                raise ZeroDivisionError("Division by zero!")
            instruction += "mod\n"
        elif p[1] == '/':
            if p[2] == 0:
                raise ZeroDivisionError("Division by zero!")
            instruction += "div\n"
        else:
            if isinstance(p[1], int):
                instruction += "pushi " + str(p[1]) + "\n"

        if function_name in functions:
            function_info = functions[function_name]
            function_params = function_info['params']
            instructions = function_info['instructions']

        instruction += 'pusha ' + function_name + '\ncall\nstop\n' + function_name + ':\n'
        for i in range(x):
            instruction += 'pushg ' + str(i + x) + '\n'
        for instr in instructions:
            instruction += instr + '\n'
        instruction += 'return\n'

    p[0] = instruction

def p_instructions7(p):
    '''instructions : instructions instruction WORD instruction
    '''
    instruction = ''
    function_name = p[3]
    function_info = functions[function_name] 
    
    if "if" in function_info and "else" in function_info and "then" in function_info:
        operador = function_info['opera']
        primparam = function_info['primeiro']
        segundparam = function_info['segundo']
        
        if operador == '<':
            operador = 'inf'
        elif operador == '>':
            operador = 'sup'
        elif operador == '=':
            operador = 'equals'
        
        instruction = 'start\npushi ' + str(p[1])+ '\npushi ' + str(p[2])+ '\n' + operador + '\njz ELSE0\njump ELSE2\nELSE0:\npushs ' + primparam + '\njump ENDIF\nELSE2:\npushs ' + segundparam + '\njump ENDIF\nENDIF:\nstop\n'

        p[0] = instruction
        return
    else:
        x = count_number(tokens)

        if isinstance(p[2], int):
            instruction += "pushi " + str(p[2]) + "\n"
        else:
            instruction += p[2]

        if p[1] == '+':
            instruction += "add\n"
        elif p[1] == '-':
            instruction += "sub\n"
        elif p[1] == '*':
            instruction += "mul\n"
        elif p[1] == '=':
            instruction += "eq\n"
        elif p[1] == '<':
            instruction += "inf\n"
        elif p[1] == '>':
            instruction += "sup\n"
        elif p[1] == '%':
            if p[2] == 0:
                raise ZeroDivisionError("Division by zero!")
            instruction += "mod\n"
        elif p[1] == '/':
            if p[2] == 0:
                raise ZeroDivisionError("Division by zero!")
            instruction += "div\n"
        else:
            if isinstance(p[1], int):
                instruction += "pushi " + str(p[1]) + "\n"

        if function_name in functions:
            function_info = functions[function_name]
            function_params = function_info['params']
            instructions = function_info['instructions']

        instruction += 'pusha ' + function_name + '\ncall\nstop\n' + function_name + ':\n'
        for i in range(x):
            instruction += 'pushg ' + str(i + x) + '\n'
        for instr in instructions:
            instruction += instr + '\n'
        instruction += 'return\n'
        
        if p[4] == '.':
            global flagN
            flagN = True
            

    p[0] = instruction

def p_instructions4(p):
    'instructions : FUNCTION_DEFINITION'
    p[0] = p[1]


def p_instructions5(p):
    '''instruction : instructions WORD instructions
    '''

    print(p[1], p[2], p[3])
    function_name = p[2]
    instruction = ''
    x = count_number(tokens)
    if isinstance(p[1], int):
        instruction += "pushi " + str(p[1]) + "\n"
    else:
        instruction += p[1]

    if function_name in functions:
        function_info = functions[function_name]
        function_params = function_info['params']
        instructions = function_info['instructions']

    instruction += 'pusha ' + function_name + '\ncall\n'
    if p[3][0] == '+':
        instruction += "add\n"
    elif p[3][0] == '-':
        instruction += "sub\n"
    elif p[3][0] == '*':
        instruction += "mul\n"
    elif p[3][0] == '%':
        if p[2] == 0:
            raise ZeroDivisionError("Division by zero!")
        instruction += "mod\n"
    elif p[3][0] == '/':
        if p[2] == 0:
            raise ZeroDivisionError("Division by zero!")
        instruction += "div\n"
    instruction += 'stop\n' + function_name + ':\n'

    for i in range(x):
        instruction += 'pushg ' + str(i + x) + '\n'
    for instr in instructions:
        instruction += 'pushi ' + instr + '\nstoreg ' + str(i + x) + '\n'
    instruction += 'return\n'

    if '+' in p[3][0]:
        global flagN
        flagN = True
    
    p[0] = instruction


def p_instructions6(p):
    'FUNCTION_DEFINITION : CONDICIONAL'
    p[0] = p[1]


def p_instruction_number(p):
    'instruction : NUMBER'
    p[0] = p[1]


def p_instruction_operator(p):
    'instruction : operator'
    p[0] = p[1]


def p_instruction_caracter(p):
    'instruction : CARACTER'
    p[0] = p[1]


def p_operator(p):
    '''operator : PLUS
                | MINUS
                | TIMES
                | DIVIDE
                | MOD
                | SUP
                | INF
                | EQUALS'''
    if p[1] == '<':
        p[0] = 'inf'
    elif p[1] == '>':
        p[0] = 'sup'
    elif p[1] == '=':
        p[0] = 'equals'
    else:    
        p[0] = p[1]


def p_instruction_print(p):
    'instruction : PRINT'
    p[0] = p[1]

def p_print(p):
    'PRINT : DOT'
    p[0] = p[1]

def p_print_num(p):
    'PRINT :  NUMBER DOT'
    p[0] = "start\npushi" + str(p[1]) + "\nwritei\nstop\n"


def p_print_string(p):
    'PRINT : DOT QUOTE words QUOTE'
    p[0] = "start\npushs\"" + p[3] + "\"\nwrites\nstop\n"


def p_print_emit(p):
    'PRINT : NUMBER EMIT'
    p[0] = "start\npushi"+ str(p[2]) +"\nstop\n"


def p_function_definition1(p):
    'FUNCTION_DEFINITION : COLON WORD LPAREN FUNCTION_PARAMS RPAREN FUNCTION_BODY SEMICOLON'

    function_name = p[2]
    function_params = p[4]
    instructions = p[6]

    functions[function_name] = {'params': function_params, 'instructions': instructions}

    p[0] = ''


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
    'FUNCTION_BODY : instructions '

    params_list = []

    if isinstance(p[1], list):
        for instr in p[1]:
            if isinstance(instr, int):
                params_list.append(str(instr))
            elif instr.startswith(('+', '-', '*', '/')):
                operator = instr[0]
                if operator == '+':
                    operator = 'add'
                elif operator == '-':
                    operator = 'sub'
                elif operator == '*':
                    operator = 'mul'
                elif operator == '%':
                    operator = 'mod'
                elif operator == '/':
                    operator = 'div'
                params_list.append(operator + '\n' + instr[1:])
            else:
                params_list.append(str(instr))
    else:
        if isinstance(p[1], int):
            params_list.append(str(p[1]))
        elif p[1].startswith(('+', '-', '*', '/')):
            operator = p[1][0]
            if operator == '+':
                operator = 'add'
            elif operator == '-':
                operator = 'sub'
            elif operator == '*':
                operator = 'mul'
            elif operator == '%':
                operator = 'mod'
            elif operator == '/':
                operator = 'div'
            params_list.append(operator + '\n' + p[1][1:])
        else:
            params_list.append(str(p[1]))

    p[0] = params_list


def p_function_body2(p):
    'FUNCTION_BODY : instruction'
    params_list = p[1]

    p[0] = params_list


def p_function_definition2(p):
    'FUNCTION_DEFINITION : COLON WORD PRINTFUNC SEMICOLON'

    function_name = p[2]
    instructions = p[3]

    functions[function_name] = (instructions)

    p[0] = ''


def p_printfunc1(p):
    'PRINTFUNC : DOT QUOTE words QUOTE'
    global flagW
    if flagW == False:
        flagW = True
        
    name = p[3]

    p[0] = name


def p_printfunc2(p):
    'PRINTFUNC : DOT QUOTE words QUOTE CARACTER'
    global flagW
    if flagW == False:
        flagW = True

    p[0] = p[3] + p[5]
    
def p_printfunc3(p):
    'PRINTFUNC : QUOTE words QUOTE'
    name = p[2]

    p[0] = name

def p_words1(p):
    'words : words WORD '
    p[0] = p[1] + ' ' + p[2]


def p_words3(p):
    'words : words WORD sinais'
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3]


def p_words2(p):
    'words : WORD'
    p[0] = p[1]


def p_functioncall(p):
    'instructions : FUNCCALL'
    p[0] = p[1]


def p_funccall(p):
    'FUNCCALL : WORD'
    function_name = p[1]
    
    if function_name in functions:
        instructions = functions[function_name]
        p[0] = 'start\npusha ' + function_name + '\ncall\nstop\n' + function_name + ':\n'

        if instructions in functions:
            secundary_func = functions[instructions]
            p[0] += 'pusha ' + instructions + '\ncall\nreturn\n' + instructions + ':\npushs "' + secundary_func + '"\nreturn\n'
        else:
            p[0] += 'pushs "' + instructions + '"\nreturn\n'


def p_sinais(p):
    """sinais : EXCLAMATION
                | INTERROGATION
    """
    p[0] = p[1]


def p_function_definition3(p):
    'FUNCTION_DEFINITION : COLON funcword SEMICOLON'

    p[0] = p[2]


def p_funcword(p):
    'funcword : WORD WORD'

    function_name = p[1]
    instructions = p[2]

    functions[function_name] = instructions

    p[0] = ''


def p_cr1(p):
    'CARACTER : CR'
    p[0] = '\n'


def p_cr2(p):
    'CARACTER : KEY'
    p[0] = '\nread\nstoreg ' + str(count_id(tokens)) + '\n'


def p_condicional1(p):
    '''
    CONDICIONAL : COLON WORD operator IF part ELSE part THEN SEMICOLON
    '''   
    
    function_name = p[2]
    OPERA = p[3]
    IF = p[4]
    PARAM1 = p[5]
    ELSE = p[6]
    PARAM2 = p[7]
    THEN = p[8]
        
    functions[function_name] = {'opera': OPERA,'primeiro': PARAM1 ,'segundo': PARAM2, 'if': IF, 'else': ELSE, 'then': THEN}
    
    p[0] = ""
    
    
    
def p_part1(p):
    '''
    part : DOT QUOTE words QUOTE
    '''
    global flagW
    flagW = True
    
    p[0] = p[2] + p[3] + p[4]

def p_part2(p):
    '''
    part : QUOTE words QUOTE
    '''
    
    p[0] = p[1] + p[2] + p[3]

def p_error(p):
    if p:
        raise SyntaxError("Syntax error at '%s'" % p.value)
    else:
        raise SyntaxError("Syntax error at EOF")


# Build the parser
parser = yacc.yacc()

f = open("result.txt", "w")
while True:
    try:
        s = input('calc > ')
        lexer.input(s)
        tokens = [token for token in lexer]
        id_count = count_id(tokens)
        if id_count > 0:
            f.write("pushi 0\n" * id_count)
        result = parser.parse(s)
        if flagN:
            result = result.replace('stop\n', 'writei\nstop\n')            
            flagN = False
        if flagW:
            result = result.replace('stop\n', 'writes\nstop\n')            

        # Verifica se a entrada define uma função
        if not s.startswith(':') and not s.endswith(';'):
            # Verifica se o resultado contém um start e um stop
            if 'start' not in result:
                result = 'start\n' + result
            if 'stop' not in result:
                result += 'stop\n'

        f.write(result)
        f.flush()

    except Exception as e:
        print(e)

f.close()
