from src.lex.lexer import Lexer, TokenType


def test_tokenize_integers():
    lexer = Lexer()
    tokens = lexer.tokenize("123 456     789")

    assert len(tokens) == 3
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == "123"
    assert tokens[1].type == TokenType.NUMBER
    assert tokens[1].value == "456"
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].value == "789"


def test_tokenize_floats():
    lexer = Lexer()
    tokens = lexer.tokenize("123.123 456.3     789.0")

    assert len(tokens) == 3
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == "123.123"
    assert tokens[1].type == TokenType.NUMBER
    assert tokens[1].value == "456.3"
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].value == "789.0"


def test_plus_sign():
    lexer = Lexer()
    tokens = lexer.tokenize("+")
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.PLUS


def test_minus_sign():
    lexer = Lexer()
    tokens = lexer.tokenize("-")
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.MINUS


def test_equal_sign():
    lexer = Lexer()
    tokens = lexer.tokenize("==")
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EQEQ

def test_equality_operators():
    lexer = Lexer()
    tokens = lexer.tokenize("== < > >= <= !=")
    assert len(tokens) == 6
    assert tokens[0].type == TokenType.EQEQ
    assert tokens[1].type == TokenType.LT
    assert tokens[2].type == TokenType.GT
    assert tokens[3].type == TokenType.GTEQ
    assert tokens[4].type == TokenType.LTEQ
    assert tokens[5].type == TokenType.NOTEQ
