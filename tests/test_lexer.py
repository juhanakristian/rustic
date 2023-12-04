from src.lex.lexer import Lexer, TokenType


def test_tokenize_numbers():
    lexer = Lexer()
    tokens = lexer.tokenize("123 456     789")

    assert len(tokens) == 3
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == "123"
    assert tokens[1].type == TokenType.NUMBER
    assert tokens[1].value == "456"
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].value == "789"