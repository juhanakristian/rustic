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