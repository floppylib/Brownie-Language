# Brownie

**Brownie** is an experimental programming language project focused on freedom, an expressive syntax, and a welcoming developer experience.

> Freedom is the guiding principle of Brownie.

## Project status

Brownie is in its early language-design and compiler-adaptation stage. Its implementation is being developed by adapting an existing compiler codebase. Brownie is not yet a released or independently bootstrapped compiler.

- **Language source extension:** `.btw`
- **Current focus:** Brownie syntax specification, lexer/parser adaptation, and compiler architecture
- **Execution targets under consideration:** Native, bytecode, and WebAssembly

## Syntax direction

Brownie's syntax takes inspiration from familiar brace-based languages while defining its own rules and identity.

Illustrative examples (the complete grammar is still under development):

```brownie
Let name = "Brownie"

Say("Hello, " + name)

function Greet(person) {
    Say("Welcome, " + person)
}
```

Semicolons are optional in the current syntax baseline. Both `Let` and `Var` declarations are supported; their final semantic distinction is still being designed.

## Development

The compiler implementation is maintained in this repository. The separate [Brownie project repository](https://github.com/floppylib/Brownie) contains project-level specifications and documentation.

Before building or contributing, consult the implementation instructions and build scripts in this repository. Some inherited build and test instructions may still apply while the compiler is being adapted.

## Project principles

- **Freedom:** give programmers meaningful choices without sacrificing clarity.
- **Clarity:** keep everyday code readable.
- **Identity:** build a language and toolchain that feel recognizably Brownie.
- **Engineering first:** preserve correctness, tests, and transparent attribution while adapting the compiler.

## Upstream foundation and attribution

Brownie's current implementation contains code inherited from an upstream compiler project. This repository retains applicable upstream copyright notices and license terms. See [UPSTREAM.md](UPSTREAM.md) and [copying.txt](copying.txt).

Brownie-specific changes and original components will be documented as development progresses.
