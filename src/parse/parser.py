import logging
import sys

from src.lex.lexer import TokenType, Lexer


class SyntaxError(Exception):
    pass


class Parser:
    def __init__(self, lexer: Lexer):
        self.current_token = None
        self.peek_token = None
        self.lexer = lexer

        self.next_token()
        self.next_token()

    def check_token(self, kind: TokenType) -> bool:
        return self.current_token.type == kind

    def check_peek(self, kind: TokenType) -> bool:
        return self.peek_token.type == kind

    def match(self, kind: TokenType):
        if not self.check_token(kind):
            raise SyntaxError(f"Expected {kind.name} but got {self.current_token.type.name}")
        self.next_token()

    def next_token(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def abort(self, message: str):
        ...

    def program(self):
        logging.info("program")
        while not self.check_token(TokenType.EOF):
            self.statement()

    def statement(self):
        if self.check_token(TokenType.PRINT):
            logging.info("print")
            self.next_token()

            if self.check_token(TokenType.STRING):
                self.next_token()
            else:
                self.expression()
        self.nl()

    def expression(self):
        ...

    def nl(self):
        logging.info("nl")

        self.match(TokenType.NEWLINE)
        while self.check_token(TokenType.NEWLINE):
            self.next_token()
