import logging
from src.lex.lexer import Lexer
from src.parse.parser import Parser


def test_print_statement():
    lexer = Lexer('print "hello"\n')
    parser = Parser(lexer)

    ast = parser.program()

    assert str(ast) == "ProgramNode([PrintNode(hello)])"


def test_basic_expressions():
    lexer = Lexer("let foo = 3 + 2\n")
    parser = Parser(lexer)
    ast = parser.program()

    assert (
        str(ast)
        == "ProgramNode([LetNode(foo, BinaryOpNode(PrimaryNode(3), TokenType.PLUS, PrimaryNode(2)))])"
    )


def test_basic_conditional():
    lexer = Lexer('let foo = 3 + 2\nif foo > 0 then\nprint "yes"\nendif\n')
    parser = Parser(lexer)
    ast = parser.program()

    assert (
        str(ast)
        == "ProgramNode([LetNode(foo, BinaryOpNode(PrimaryNode(3), TokenType.PLUS, PrimaryNode(2))), IfNode(ComparisonNode(PrimaryNode(foo), TokenType.GT, PrimaryNode(0)), [PrintNode(yes)])])"
    )


def test_undeclared_variable():
    lexer = Lexer("print foo\n")
    parser = Parser(lexer)
    try:
        parser.program()
        assert False
    except Exception as e:
        assert str(e) == "Referencing variable before assignment: foo"


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
    ast = parser.program()
    logging.debug(str(ast))

    assert (
        str(ast)
        == "ProgramNode([PrintNode(How many fibonacci numbers do you want?), InputNode(nums), PrintNode(), LetNode(a, PrimaryNode(0)), LetNode(b, PrimaryNode(1)), WhileNode(ComparisonNode(PrimaryNode(nums), TokenType.GT, PrimaryNode(0)), [PrintNode(PrimaryNode(a)), LetNode(c, BinaryOpNode(PrimaryNode(a), TokenType.PLUS, PrimaryNode(b))), LetNode(a, PrimaryNode(b)), LetNode(b, PrimaryNode(c)), LetNode(nums, BinaryOpNode(PrimaryNode(nums), TokenType.MINUS, PrimaryNode(1)))])])"
    )
