import sys
import enum

class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3

class Token:
    type: TokenType
    value: str

    def __init__(self, type: TokenType, value: str):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    source: str

    current_position: int
    current_char: str

    def __init__(self):
        self.current_char = ""
        self.current_position = -1

    def tokenize(self, input: str) -> list[Token]:
        self.source = input
        self.next_char()
        tokens = []
        while self.current_char != "\0" or len(tokens) > 3:
            tokens.append(self.next_token())
        return tokens

    def consume_whitespace(self):
        while self.current_char == " " or self.current_char == "\t" or self.current_char == "\n":
            self.next_char()

    def next_token(self) -> Token:
        self.consume_whitespace()
        token = None
        if self.current_char.isdigit():
            position = self.current_position
            while self.peek().isdigit():
                self.next_char()
            value = self.source[position : self.current_position + 1]
            token = Token(TokenType.NUMBER, value)
        elif self.current_char == "\0":
            token = Token(TokenType.EOF, "")
        else:
            self.abort("Unknown token: " + self.current_char)

        self.next_char()
        return token

    def next_char(self) -> str:
        self.current_position += 1
        if self.current_position >= len(self.source):
            self.current_char = "\0"
        else:
            self.current_char = self.source[self.current_position]
        return self.current_char

    def peek(self) -> str:
        if self.current_position + 1 >= len(self.source):
            return "\0"
        return self.source[self.current_position + 1]

    def abort(self, message: str):
        sys.exit("Lexing error. " + message)




