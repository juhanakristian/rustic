# Rustic

Rustic is a TinyBASIC subset compiler to Rust written in Python. I built Rustic in order to learn the basics of compilers and parsers. It is not meant to be feature complete or useful in any other way.

The lexer and parser are based on Austin Henley's [Teeny Tiny Compiler blog series](https://austinhenley.com/blog/teenytinycompiler1.html). Instead of emitting C code from the parser I decided to create an AST and a Rust emitter.



## Usage

```sh
$ python rustic <source>
```


