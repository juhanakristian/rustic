import enum

class Token(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
class Lexer:
    source: str
    def __init__(self):
        ...

    def tokenize(self, input: str) -> list[Token]:
        ...

    def next_token(self) -> Token:
        ...




