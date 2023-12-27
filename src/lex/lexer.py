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
        """
        Tokenize the input string.
        :param input: Tiny BASIC source code
        :return: List of tokens
        """
        self.current_char = ""
        self.current_position = -1
        self.source = input
        self.next_char()
        tokens = []
        while self.current_char != "\0" or len(tokens) > 3:
            tokens.append(self.next_token())
        return tokens

    def consume_whitespace(self):
        """
        Consume all whitespace until the next non-whitespace character.
        """
        while self.current_char == " " or self.current_char == "\t" or self.current_char == "\n":
            self.next_char()

    def next_token(self) -> Token:
        """
        Get the next token in the source string.
        :return:
        """
        self.consume_whitespace()
        token = None
        if self.current_char.isdigit():
            position = self.current_position
            # Continue reading digits until we hit a non-digit character
            while self.peek().isdigit():
                self.next_char()
            # Get the entire number
            value = self.source[position: self.current_position + 1]
            # If the next character is a dot, we're dealing with a float
            if self.peek() == ".":
                self.next_char()
                while self.peek().isdigit():
                    self.next_char()
                value = self.source[position: self.current_position + 1]
            token = Token(TokenType.NUMBER, value)
        elif self.current_char == "\0":
            token = Token(TokenType.EOF, "")
        else:
            self.abort("Unknown token: " + self.current_char)

        self.next_char()
        return token

    def next_char(self) -> str:
        """
        Get the next character in the source string.
        Moves the current position forward.
        :return: Next character in the source string
        """
        self.current_position += 1
        # If we've reached the end of the source string, set the null character as the current character
        if self.current_position >= len(self.source):
            self.current_char = "\0"
        else:
            self.current_char = self.source[self.current_position]
        return self.current_char

    def peek(self) -> str:
        """
        Get the next character in the source string without moving the current position forward.
        :return: Next character in the source string
        """
        if self.current_position + 1 >= len(self.source):
            return "\0"
        return self.source[self.current_position + 1]

    @staticmethod
    def abort(message: str):
        """
        Abort lexing.
        :param message: Error message
        :return:
        """
        sys.exit("Lexing error. " + message)
