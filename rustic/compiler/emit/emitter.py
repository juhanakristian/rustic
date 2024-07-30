from ..lex.lexer import TokenType
from ..ast.nodes import (
    ASTNode,
    BinaryOpNode,
    ComparisonNode,
    IfNode,
    InputNode,
    LetNode,
    PrimaryNode,
    PrintNode,
    ProgramNode,
    WhileNode,
)

TAB_WIDTH = 2


class EmitError(Exception):
    pass


def with_indent(input: str, indent: int = 0):
    return f"{input:>{indent}}"


class Emitter:
    ast: ProgramNode
    output: str

    symbols: list[str]

    def __init__(self, ast: ProgramNode):
        self.ast = ast
        self.output = ""
        self.symbols = []

    def emit(self) -> str:
        output = ""

        for statement in self.ast.statements:
            output += self.emit_node(statement, 1)

        imports = "use std::io::stdin;\n"
        program_code = "fn main() {\n" + output + "}"

        return f"{imports} {program_code}"

    def emit_node(self, node: ASTNode, indent: int = 0) -> str:
        if isinstance(node, PrintNode):
            if isinstance(node.value, ASTNode):
                return with_indent(
                    f'println!("{{}}", {self.emit_node(node.value)});\n', indent
                )
            return with_indent(f'println!("{node.value}");\n', indent)
        elif isinstance(node, LetNode):
            if node.variable in self.symbols:
                return with_indent(
                    f"{node.variable} = {self.emit_node(node.expression)};\n", indent
                )

            self.symbols.append(node.variable)

            return with_indent(
                f"let mut {node.variable} = {self.emit_node(node.expression)};\n",
                indent,
            )
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

            return with_indent(
                f"if {comparison} {{\n{with_indent(then_block, indent + 1)}}}\n", indent
            )
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
        elif isinstance(node, WhileNode):
            comparison = self.emit_node(node.condition)

            body = ""
            for block_node in node.body:
                body += self.emit_node(block_node)

            return with_indent(
                f"while {comparison} {{\n{with_indent(body, indent + 1)}}}\n", indent
            )
        elif isinstance(node, InputNode):
            input_variable = with_indent(
                f"let mut {node.variable}_input = String::new();", indent
            )
            input = with_indent(
                f"stdin().read_line(&mut {node.variable}_input);", indent
            )
            variable = with_indent(
                f'let mut {node.variable}: i32 = {node.variable}_input.trim().parse().expect("Input is not a integer");',
                indent,
            )

            self.symbols.append(node.variable)

            return f"{input_variable}\n{input}\n{variable}\n"

        return ""
