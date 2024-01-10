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


def test_asterisk():
    lexer = Lexer()
    tokens = lexer.tokenize("*")
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.ASTERISK


def test_slash():
    lexer = Lexer()
    tokens = lexer.tokenize("/")
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.SLASH


def test_newline():
    lexer = Lexer()
    tokens = lexer.tokenize("\n")
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.NEWLINE


def test_control_flow_keywords():
    lexer = Lexer()
    tokens = lexer.tokenize("if endif while repeat endwhile then goto")
    assert len(tokens) == 7
    assert tokens[0].type == TokenType.IF
    assert tokens[1].type == TokenType.ENDIF
    assert tokens[2].type == TokenType.WHILE
    assert tokens[3].type == TokenType.REPEAT
    assert tokens[4].type == TokenType.ENDWHILE
    assert tokens[5].type == TokenType.THEN
    assert tokens[6].type == TokenType.GOTO


def test_keywords():
    lexer = Lexer()
    tokens = lexer.tokenize("label print input let")
    assert len(tokens) == 4
    assert tokens[0].type == TokenType.LABEL
    assert tokens[1].type == TokenType.PRINT
    assert tokens[2].type == TokenType.INPUT
    assert tokens[3].type == TokenType.LET


def test_identifiers():
    lexer = Lexer()
    tokens = lexer.tokenize("a b c")
    assert len(tokens) == 3
    assert tokens[0].type == TokenType.IDENT
    assert tokens[0].value == "a"
    assert tokens[1].type == TokenType.IDENT
    assert tokens[1].value == "b"
    assert tokens[2].type == TokenType.IDENT
    assert tokens[2].value == "c"

