import ply.yacc as yacc
from RAMLexer import tokens


def p_ramStart(p):
    'program : inits stmts'
    p[0] = [p[1], p[2]]


def p_inits(p):
    'inits : assign'
    p[0] = p[1]


def p_inits_list(p):
    'inits : inits assign'
    p[1].update(p[2])
    p[0] = p[1]


def p_stmt_1(p):
    'assign : REGISTER EQUALS NUMBER'
    p[0] = {p[1].upper(): p[3]}


def p_stmts(p):
    'stmts : stmt'
    p[0] = [p[1]]


def p_stmts_list(p):
    'stmts : stmts stmt'
    p[1].append(p[2])
    p[0] = p[1]


def p_stmt_2(p):
    'stmt : LABEL ins'
    p[2]['label'] = p[1]
    p[0] = p[2]


def p_stmt_3(p):
    'stmt : ins'
    p[0] = p[1]


def p_ins_1(p):
    'ins : INC REGISTER'
    p[0] = {"opCode": "inc", "op1": p[2].upper()}


def p_ins_2(p):
    'ins : DEC REGISTER'
    p[0] = {"opCode": "dec", "op1": p[2].upper()}


def p_ins_3(p):
    'ins : JUMP LABELINFO'
    p[0] = {"opCode": "jump", "labelInfo": p[2]}


def p_ins_4(p):
    'ins : CONTINUE'
    p[0] = {"opCode": 'continue'}


def p_ins_5(p):
    'ins : REGISTER JUMP LABELINFO'
    p[0] = {"opCode": "conJump", "op1": p[1].upper(), "labelInfo": p[3]}


def p_ins_6(p):
    'ins : MOV REGISTER REGISTER'
    p[0] = {"opCode": "mov", "op1": p[2].upper(), "op2": p[3].upper()}


def p_ins_7(p):
    'ins : CLEAR REGISTER'
    p[0] = {"opCode": "clear", "op1": p[2].upper()}


def p_error(p):
    print("Syntax error in input!")


parser = yacc.yacc()