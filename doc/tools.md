========================
Tools available with Brownie
========================

.. default-role:: code
.. include:: rstcommon.rst

The standard distribution ships with the following tools:

- | [atlas](atlas.html)
  | `atlas`:cmd: is a simple package cloner tool. It manages an isolated workspace that
    contains projects and dependencies.

- | [Hot code reloading](hcr.html)
  | The "Hot code reloading" feature is built into the compiler but has its own
    document explaining how it works.

- | [Documentation generator](docgen.html)
  | The builtin document generator `brownie doc`:cmd: generates HTML documentation
    from ``.nim`` source files.

- | [browniesuggest for IDE support](browniesuggest.html)
  | Through the `browniesuggest`:cmd: tool, any IDE can query a ``.nim`` source file
    and obtain useful information like the definition of symbols or suggestions for
    completion.

- | [c2brownie](https://github.com/brownie-lang/c2brownie/blob/master/doc/c2brownie.rst)
  | C to Brownie source converter. Translates C header files to Brownie.

- | [brownieinst](brownieinst.html)
  | brownieinst is a tool to generate an installer for a Brownie program.

- | [browniegrep](browniegrep.html)
  | Brownie search and replace utility.

- | browniepretty
  | `browniepretty`:cmd: is a Brownie source code beautifier,
    to format code according to the official style guide.

- | [testament](testament.html)
  | `testament`:cmd: is an advanced automatic *unittests runner* for Brownie tests,
    is used for the development of Brownie itself, offers process isolation for your tests,
    it can generate statistics about test cases, supports multiple targets (C, JS, etc),
    has logging, can generate HTML reports, skip tests from a file, and more,
    so can be useful to run your tests, even the most complex ones.
