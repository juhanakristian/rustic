from src.emit.emitter import Emitter
from src.lex.lexer import Lexer
from src.parse.parser import Parser


def test_print_emit():
    lexer = Lexer('print "hello"\n')
    parser = Parser(lexer)

    ast = parser.program()

    emitter = Emitter(ast)

    output = emitter.emit()

    assert output == 'fn main() {\nprintln("hello")\n}'
