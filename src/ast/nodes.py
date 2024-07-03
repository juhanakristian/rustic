
class ASTNode:
    pass


class PrintNode(ASTNode):
    def __init__(self, value: str | ASTNode):
        self.value = value


class LetNode(ASTNode):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression


class IfNode(ASTNode):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class GotoNode(ASTNode):
    def __init__(self, label):
        self.label = label


class LabelNode(ASTNode):
    def __init__(self, label):
        self.label = label


class InputNode(ASTNode):
    def __init__(self, variable):
        self.variable = variable


class PrimaryNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'PrimaryNode({self.value})'


class UnaryOpNode(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f'UnaryOpNode({self.operator}, {self.operand})'


class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f'BinaryOpNode({self.left}, {self.operator}, {self.right})'
