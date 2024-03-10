import logging
from src.lex.lexer import Lexer
from src.parse.parser import Parser


def test_print_statement():
    lexer = Lexer('print "hello"\n')
    parser = Parser(lexer)

    parser.program()


def test_goto_statement():
    lexer = Lexer('LABEL loop\nprint "hello"\ngoto loop\n')
    parser = Parser(lexer)

    parser.program()

def test_basic_expressions():
    lexer = Lexer('let foo = 3 + 2\n')
    parser = Parser(lexer)
    parser.program()

def test_basic_conditional():
    lexer = Lexer('let foo = 3 + 2\nif foo > 0 then\nprint "yes"\nendif\n')
    parser = Parser(lexer)
    parser.program()


def test_undeclared_variable():
    lexer = Lexer('print foo\n')
    parser = Parser(lexer)
    try:
        parser.program()
        assert False
    except Exception as e:
        assert str(e) == "Variable foo not declared"

def test_fibonacci():
    code = """
    PRINT "How many fibonacci numbers do you want?"
    INPUT nums
    PRINT ""

    LET a = 0
    LET b = 1
    WHILE nums > 0 REPEAT
        PRINT a
        LET c = a + b
        LET a = b
        LET b = c
        LET nums = nums - 1
    ENDWHILE
    """

    lexer = Lexer(code)
    parser = Parser(lexer)
    parser.program()