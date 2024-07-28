from src.lex.lexer import TokenType
from src.ast.nodes import (
    ASTNode,
    BinaryOpNode,
    LetNode,
    PrimaryNode,
    PrintNode,
    ProgramNode,
)


class Emitter:
    ast: ProgramNode
    output: str

    def __init__(self, ast: ProgramNode):
        self.ast = ast
        self.output = ""

    def emit(self) -> str:
        output = ""

        for statement in self.ast.statements:
            output += self.emit_node(statement)

        program_code = "fn main() {\n" + output + "\n}"

        return program_code

    def emit_node(self, node: ASTNode) -> str:
        if isinstance(node, PrintNode):
            return f'println("{node.value}")'
        elif isinstance(node, LetNode):
            return f"let {node.variable} = {self.emit_node(node.expression)}"
        elif isinstance(node, PrimaryNode):
            return f"{node.value}"
        elif isinstance(node, BinaryOpNode):
            operator = "+"
            if node.operator == TokenType.PLUS:
                operator = "+"
            elif node.operator == TokenType.MINUS:
                operator = "-"

            return (
                f"{self.emit_node(node.left)} {operator} {self.emit_node(node.right)}"
            )

        return ""
