
class ASTNode:
    pass


class PrintNode(ASTNode):
    def __init__(self, value):
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


