import sys
import enum


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3

    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111

    # Operators
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211

    @staticmethod
    def is_keyword(token: str) -> bool:
        for kind in TokenType:
            if kind.name == token.upper() and 101 <= kind.value <= 111:
                return True
        return False


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

    def __init__(self, input: str):
        self.current_char = ""
        self.current_position = -1
        self.source = input
        self.next_char()

    def tokenize(self) -> list[Token]:
        """
        Tokenize the input string.
        :param input: Tiny BASIC source code
        :return: List of tokens
        """
        tokens = []
        while self.current_char != "\0":
            tokens.append(self.next_token())
        return tokens

    def consume_whitespace(self):
        """
        Consume all whitespace until the next non-whitespace character.
        """
        while self.current_char == " " or self.current_char == "\t" or self.current_char == "\r":
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
                # Continue reading digits until the float part ends
                while self.peek().isdigit():
                    self.next_char()
                value = self.source[position: self.current_position + 1]
            token = Token(TokenType.NUMBER, value)
        elif self.current_char == "+":
            token = Token(TokenType.PLUS, self.current_char)
        elif self.current_char == "-":
            token = Token(TokenType.MINUS, self.current_char)
        elif self.current_char == "*":
            token = Token(TokenType.ASTERISK, self.current_char)
        elif self.current_char == "/":
            token = Token(TokenType.SLASH, self.current_char)
        elif self.current_char == "=":
            if self.peek() == "=":
                self.next_char()
                token = Token(TokenType.EQEQ, "==")
            else:
                token = Token(TokenType.EQ, self.current_char)
        elif self.current_char == "<":
            if self.peek() == "=":
                self.next_char()
                token = Token(TokenType.LTEQ, "<=")
            else:
                token = Token(TokenType.LT, self.current_char)
        elif self.current_char == ">":
            if self.peek() == "=":
                self.next_char()
                token = Token(TokenType.GTEQ, ">=")
            else:
                token = Token(TokenType.GT, self.current_char)
        elif self.current_char == "!":
            if self.peek() == "=":
                self.next_char()
                token = Token(TokenType.NOTEQ, "!=")
            else:
                self.abort("Expected !=, got !" + self.peek())
        elif self.current_char.isalnum():
            position = self.current_position
            # Continue reading letters and digits until we hit a non-letter/digit character
            while self.peek().isalnum():
                self.next_char()
            # Get the entire word
            value = self.source[position: self.current_position + 1]
            # Check if the word is a keyword
            if TokenType.is_keyword(value):
                token = Token(TokenType[value.upper()], value)
            else:
                token = Token(TokenType.IDENT, value)
        elif self.current_char == "\"":
            self.next_char()
            position = self.current_position
            # Continue reading characters until we hit a non-letter/digit character
            while self.current_char != "\"":
                if (self.current_char == "\r" or self.current_char == "\n" or self.current_char == "\t"
                        or self.current_char == "\\" or self.current_char == "%"):
                    self.abort("Illegal character in string.")
                self.next_char()
            # Get the entire word
            value = self.source[position: self.current_position]
            token = Token(TokenType.STRING, value)
        elif self.current_char == "\n":
            token = Token(TokenType.NEWLINE, self.current_char)
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
