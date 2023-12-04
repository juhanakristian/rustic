import argparse

from lexer import Lexer

arg_parser = argparse.ArgumentParser(description='Rustic: A Rusty Python Interpreter')
arg_parser.add_argument('input', type=str, nargs='?', help='The file to interpret')
arg_parser.add_argument("output", type=str, nargs="?", help="The file to output to")

args = arg_parser.parse_args()

