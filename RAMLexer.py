import ply.lex as lex

tokens = [
    'REGISTER', 'EQUALS', 'LABEL', 'INC', 'JUMP', 'DEC', 'CONTINUE', 'MOV',
    'LABELINFO', 'NUMBER', 'CLEAR'
]

t_REGISTER = r'[rR][0-9]+'
t_EQUALS = r'[=]'
t_LABEL = r'[nN][0-9]+'
t_INC = r'[iI][nN][cC]'
t_JUMP = r'[jJ][mM][pP]'
t_DEC = r'[dD][eE][cC]'
t_CONTINUE = r'[cC][oO][nN][tT][iI][nN][uU][eE]'
t_MOV = r'[mM][oO][vV]'
t_NUMBER = r'[0-9]+'
t_LABELINFO = r'[nN][0-9]+[aAbB]'
t_CLEAR = r'[cC][lL][rR]'

#ignore tokens
t_ignore = " \r\n\t"
t_ignore_COMMENT = r"\#.*"
t_ignore_COMMA = r"[,]"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    #t.lexer.skip(1)
    raise Exception('LEXER ERROR')


lexer = lex.lex()

# Test it out
data = '''
r1=2
r2=4

n0 inc r2
jmp n0
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
