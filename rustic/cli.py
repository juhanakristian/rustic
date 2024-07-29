import sys
import argparse

from emit.emitter import Emitter
from lex.lexer import Lexer
from parse.parser import Parser


class Rustic:
    def compile(self, input: str) -> str:
        lexer = Lexer('print "hello"\n')
        parser = Parser(lexer)

        ast = parser.program()

        emitter = Emitter(ast)
        return emitter.emit()


def cli():
    arg_parser = argparse.ArgumentParser(
        description="Rustic: A Rusty Python Interpreter"
    )
    arg_parser.add_argument("input", type=str, nargs="?", help="The file to interpret")
    arg_parser.add_argument("output", type=str, nargs="?", help="The file to output to")

    args = arg_parser.parse_args()

    if args.input is None:
        arg_parser.print_help()
        sys.exit(1)

    input_data = None
    with open(args.input, "r") as f:
        input_data = f.read()

    compiler = Rustic()
    result = compiler.compile(input_data)

    if args.output is None:
        print(result)
        sys.exit(0)

    with open(args.output, "wt") as f:
        f.write(result)
