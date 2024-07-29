from src.emit.emitter import Emitter
from src.lex.lexer import Lexer
from src.parse.parser import Parser


def test_print_emit():
    lexer = Lexer('print "hello"\n')
    parser = Parser(lexer)

    ast = parser.program()

    emitter = Emitter(ast)

    output = emitter.emit()

    assert output == 'fn main() {\nprintln("hello");\n}'


def test_basic_expressions_emit():
    lexer = Lexer("let foo = 3 + 2\n")
    parser = Parser(lexer)
    ast = parser.program()

    emitter = Emitter(ast)
    output = emitter.emit()

    assert output == "fn main() {\nlet foo = 3 + 2;\n}"


def test_basic_conditional_emit():
    lexer = Lexer('let foo = 3 + 2\nif foo > 0 then\nprint "yes"\nendif\n')
    parser = Parser(lexer)
    ast = parser.program()

    emitter = Emitter(ast)
    output = emitter.emit()

    assert (
        output == 'fn main() {\nlet foo = 3 + 2;\nif foo > 0 {\nprintln("yes");\n}\n}'
    )
