from src.ast.nodes import ASTNode, PrintNode, ProgramNode


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

        return ""
