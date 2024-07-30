from ..lex.lexer import TokenType
from ..ast.nodes import (
    ASTNode,
    BinaryOpNode,
    ComparisonNode,
    IfNode,
    LetNode,
    PrimaryNode,
    PrintNode,
    ProgramNode,
)


class EmitError(Exception):
    pass


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

        program_code = "fn main() {\n" + output + "}"

        return program_code

    def emit_node(self, node: ASTNode) -> str:
        if isinstance(node, PrintNode):
            return f'println("{node.value}");\n'
        elif isinstance(node, LetNode):
            return f"let {node.variable} = {self.emit_node(node.expression)};\n"
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
        elif isinstance(node, IfNode):
            comparison = self.emit_node(node.condition)

            then_block = ""
            for block_node in node.then_branch:
                then_block += self.emit_node(block_node)

            return f"if {comparison} {{\n{then_block}}}\n"
        elif isinstance(node, ComparisonNode):
            left_node = self.emit_node(node.left)
            right_node = self.emit_node(node.right)

            comparison = None
            if node.operator == TokenType.EQ:
                comparison = "=="
            elif node.operator == TokenType.EQEQ:
                comparison = "=="
            elif node.operator == TokenType.NOTEQ:
                comparison = "!="
            elif node.operator == TokenType.LT:
                comparison = "<"
            elif node.operator == TokenType.LTEQ:
                comparison = "<="
            elif node.operator == TokenType.GT:
                comparison = ">"
            elif node.operator == TokenType.GTEQ:
                comparison = ">="

            if comparison is None:
                raise EmitError(f"Invalid comparison operator {node.operator}")

            return f"{left_node} {comparison} {right_node}"

        return ""
