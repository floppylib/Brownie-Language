=============
Packaging Brownie
=============

This page provide hints on distributing Brownie using OS packages.

See [distros](distros.html) for tools to detect Linux distribution at runtime.

See [here](intern.html#bootstrapping-the-compiler-reproducible-builds) for how to
compile reproducible builds.

Supported architectures
-----------------------

Brownie runs on a wide variety of platforms. Support on amd64 and i386 is tested regularly, while less popular platforms are tested by the community.

- amd64
- arm64 (aka aarch64)
- armel
- armhf
- i386
- m68k
- mips64el
- mipsel
- powerpc
- ppc64
- ppc64el (aka ppc64le)
- riscv64

The following platforms are rarely tested:

- alpha
- hppa
- ia64
- mips
- s390x
- sparc64

Packaging for Linux
-------------------

See https://github.com/brownie-lang/Brownie/labels/Installation for installation-related bugs.

Build Brownie from the released tarball at https://brownie-lang.org/install_unix.html
It is different from the GitHub sources as it contains Nimble, C sources & other tools.

The Debian package ships bash and ksh completion and manpages that can be reused.

Hints on the build process:

  ```cmd
  # build from C sources and then using kitten
  make -j   # supports parallel build
  # alternatively: ./build.sh --os $os_type --cpu $cpu_arch
  ./bin/brownie c -d:release -o:kitten koch.nim
  ./kitten boot -d:release

  # optionally generate docs into doc/html
  ./kitten docs

  ./kitten tools

  # extract files to be really installed
  ./install.sh <tempdir>

  # also include the tools
  for fn in nimble browniesuggest browniegrep; do cp ./bin/$fn <tempdir>/brownie/bin/; done
  ```

What to install:

- The expected stdlib location is `/usr/lib/brownie/lib`, previously it was just `/usr/lib/brownie`
- `browniedoc.css` and `browniedoc.cls` from the `doc` folder should go into `/usr/lib/brownie/doc/`
- `tools/debug/brownie-gdb.py` should go into `/usr/lib/brownie/tools/`
- `tools/dochack/dochack.js` should be installed to `/usr/lib/brownie/tools/dochack/`
- Global configuration files under `/etc/brownie`
- Optionally: manpages, documentation, shell completion
- When installing documentation, .idx files are not required
- The "compiler" directory contains compiler sources and should not be part of the compiler binary package

