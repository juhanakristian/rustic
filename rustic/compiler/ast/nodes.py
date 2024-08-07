import enum
from ..lex.lexer import TokenType


class Operator(enum.Enum):
    PLUS = 100
    MINUS = 101
    ASTERISK = 102
    SLASH = 103


class Comparator(enum.Enum):
    EQ = 201
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211


class ASTNode:
    pass


class PrintNode(ASTNode):
    def __init__(self, value: str | ASTNode):
        self.value = value

    def __repr__(self):
        return f"PrintNode({self.value})"


class InputNode(ASTNode):
    def __init__(self, variable):
        self.variable = variable

    def __repr__(self):
        return f"InputNode({self.variable})"


class LetNode(ASTNode):
    def __init__(self, variable: str, expression: ASTNode):
        self.variable = variable
        self.expression = expression

    def __repr__(self):
        return f"LetNode({self.variable}, {self.expression})"


class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, then_branch: list[ASTNode]):
        self.condition = condition
        self.then_branch = then_branch

    def __repr__(self):
        return f"IfNode({self.condition}, {self.then_branch})"


class ComparisonNode:
    def __init__(self, left: ASTNode, operator: TokenType, right: ASTNode):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"ComparisonNode({self.left}, {self.operator}, {self.right})"


class WhileNode(ASTNode):
    def __init__(self, condition: ASTNode, body: list[ASTNode]):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileNode({self.condition}, {self.body})"


class PrimaryNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"PrimaryNode({self.value})"


class UnaryOpNode(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"UnaryOpNode({self.operator}, {self.operand})"


class BinaryOpNode(ASTNode):
    def __init__(self, left: ASTNode, operator, right: ASTNode):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinaryOpNode({self.left}, {self.operator}, {self.right})"


class ProgramNode(ASTNode):
    def __init__(self, statements: list[ASTNode]):
        self.statements = statements

    def __repr__(self):
        return f"ProgramNode({self.statements})"
