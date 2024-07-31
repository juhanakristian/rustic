# Rustic

Rustic is a TinyBASIC subset compiler to Rust written in Python. I built Rustic in order to learn the basics of compilers and parsers. It is not meant to be feature complete or useful in any other way.

The lexer and parser are based on Austin Henley's [Teeny Tiny Compiler blog series](https://austinhenley.com/blog/teenytinycompiler1.html). Instead of emitting C code from the parser I decided to create an AST and a Rust emitter.


## Usage

```sh
$ python rustic <source>
```


## Examples

Here are some basic(!) examples of the Rust code Rustic produces.

conditional.bs
````basic
LET foo = 3 + 2

IF foo > 0 THEN
  PRINT "YES!"
ENDIF
``````

Compiles to 
````rust
use std::io::stdin;
fn main() {
    let mut foo = 3 + 2;
    if foo > 0 {
        println!("YES!");
    }
}
``````


fibonacci.bs
```basic
PRINT "How many fibonacci numbers do you want?"
INPUT nums
PRINT ""

LET a = 0
LET b = 1
WHILE nums > 0 REPEAT
    PRINT a
    LET c = a + b
    LET a = b
    LET b = c
    LET nums = nums - 1
ENDWHILE

```

Compiles to
```rust
use std::io::stdin;
fn main() {
    println!("How many fibonacci numbers do you want?");
    let mut nums_input = String::new();
    stdin().read_line(&mut nums_input);
    let mut nums: i32 = nums_input.trim().parse().expect("Input is not a integer");
    println!("");
    let mut a = 0;
    let mut b = 1;
    while nums > 0 {
        println!("{}", a);
        let mut c = a + b;
        a = b;
        b = c;
        nums = nums - 1;
    }
}
```

average.bs

```basic
LET a = 0
WHILE a < 1 REPEAT
    PRINT "Enter number of scores: "
    INPUT a
ENDWHILE

LET b = 0
LET s = 0
PRINT "Enter one value at a time: "
WHILE b < a REPEAT
    INPUT c
    LET s = s + c
    LET b = b + 1
ENDWHILE

PRINT "Average: "
PRINT s / a

```

Compiles to
```rust
use std::io::stdin;
fn main() {
    let mut a = 0;
    while a < 1 {
        println!("Enter number of scores: ");
        let mut a_input = String::new();
        stdin().read_line(&mut a_input);
        a = a_input.trim().parse().expect("Input is not a integer");
    }
    let mut b = 0;
    let mut s = 0;
    println!("Enter one value at a time: ");
    while b < a {
        let mut c_input = String::new();
        stdin().read_line(&mut c_input);
        let mut c: i32 = c_input.trim().parse().expect("Input is not a integer");
        s = s + c;
        b = b + 1;
    }
    println!("Average: ");
    println!("{}", s / a);
}
```
