import logging
import sys

from src.ast.nodes import ASTNode, PrintNode, BinaryOpNode, UnaryOpNode, PrimaryNode, IfNode, ComparisonNode
from src.lex.lexer import TokenType, Lexer


class SyntaxError(Exception):
    pass


class Parser:
    def __init__(self, lexer: Lexer):
        self.current_token = None
        self.peek_token = None
        self.lexer = lexer

        self.symbols = set()
        self.labels_declared = set()
        self.labels_gotoed = set()

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
        raise SyntaxError(message)

    def program(self):
        logging.info("program")
        # Consume all newlines at the start
        while self.check_token(TokenType.NEWLINE):
            self.next_token()

        while not self.check_token(TokenType.EOF):
            self.statement()

        for label in self.labels_gotoed:
            if label not in self.labels_declared:
                self.abort(f"Attempting to GOTO to undeclared label {label}")

    def statement(self) -> ASTNode:
        if self.check_token(TokenType.PRINT):
            logging.info("print")
            self.next_token()

            if self.check_token(TokenType.STRING):
                value = self.current_token.value
                self.next_token()
                return PrintNode(value)
            else:
                expression = self.expression()
                return PrintNode(expression)
        elif self.check_token(TokenType.IF):
            logging.info("if")
            self.next_token()
            condition = self.comparison()

            self.match(TokenType.THEN)
            self.nl()

            then_branch = []
            while not self.check_token(TokenType.ENDIF):
                then_branch.append(self.statement())

            self.match(TokenType.ENDIF)
            return IfNode(condition, then_branch)
        elif self.check_token(TokenType.WHILE):
            logging.info("while")
            self.next_token()
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()

            while not self.check_token(TokenType.ENDWHILE):
                self.statement()
            self.match(TokenType.ENDWHILE)
        elif self.check_token(TokenType.LABEL):
            logging.info("label")
            self.next_token()
            # Check if label already exists
            if self.current_token.value in self.labels_declared:
                self.abort(f"Label {self.current_token.value} already exists")

            self.labels_declared.add(self.current_token.value)
            self.match(TokenType.IDENT)
        elif self.check_token(TokenType.GOTO):
            logging.info("goto")
            self.next_token()
            self.labels_gotoed.add(self.current_token.value)
            self.match(TokenType.IDENT)
        elif self.check_token(TokenType.LET):
            logging.info("let")
            self.next_token()
            if self.current_token.value not in self.symbols:
                self.symbols.add(self.current_token.value)

            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            return self.expression()
        elif self.check_token(TokenType.INPUT):
            logging.info("input")
            self.next_token()
            if self.current_token.value not in self.symbols:
                self.symbols.add(self.current_token.value)

            self.match(TokenType.IDENT)
        else:
            self.abort(f"Invalid statement at {self.current_token.value}")

        self.nl()

    def term(self) -> ASTNode:
        """
        term ::= unary {( "*" | "/" ) unary}
        """
        logging.info("term")
        left = self.unary()
        while self.check_token(TokenType.ASTERISK) or self.check_token(TokenType.SLASH):
            operator = self.current_token.type
            self.next_token()
            right = self.unary()
            left = BinaryOpNode(left, operator, right)

        return left

    def unary(self) -> ASTNode:
        """
        unary ::= ["+" | "-"] primary
        """
        logging.info("unary")
        if self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            operator = self.current_token.type
            self.next_token()
            operand = self.primary()
            return UnaryOpNode(operator, operand)

        return self.primary()

    def primary(self) -> ASTNode:
        """
        primary ::= number | ident
        """
        logging.info("primary")
        if self.check_token(TokenType.NUMBER):
            value = self.current_token.value
            self.next_token()
            return PrimaryNode(value)
        elif self.check_token(TokenType.IDENT):
            if self.current_token.value not in self.symbols:
                self.abort(f"Referencing variable before assignment: {self.current_token.value}")
            value = self.current_token.value
            self.next_token()
            return PrimaryNode(value)
        else:
            self.abort(f"Unexpected token at {self.current_token.value}")

    def expression(self) -> ASTNode:
        """
        expression ::= term {( "-" | "+" ) term}
        """
        logging.info("expression")
        first_term = self.term()
        while self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            operator = self.current_token.type
            self.next_token()
            next_term = self.term()
            first_term = BinaryOpNode(first_term, operator, next_term)

        return first_term


    def comparison(self):
        """
        comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
        """
        logging.info("comparison")
        left = self.expression()

        if self.is_comparison_operator():
            operator = self.current_token.type
            self.next_token()
            right = self.expression()
            left = ComparisonNode(left, operator, right)
        else:
            self.abort(f"Expected comparison operator at {self.current_token.value}")

        while self.is_comparison_operator():
            operator = self.current_token.type
            self.next_token()
            right = self.expression()
            left = ComparisonNode(left, operator, right)

        return left

    def is_comparison_operator(self) -> bool:
        return self.check_token(TokenType.EQEQ) or self.check_token(TokenType.NOTEQ) or self.check_token(
            TokenType.LT) or self.check_token(TokenType.LTEQ) or self.check_token(TokenType.GT) or self.check_token(
            TokenType.GTEQ)

    def nl(self):
        logging.info("nl")

        self.match(TokenType.NEWLINE)
        while self.check_token(TokenType.NEWLINE):
            self.next_token()
