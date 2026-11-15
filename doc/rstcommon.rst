..
  Usage of this file:
     Add this in the beginning of *.rst file:

         .. default-role:: code
         .. include:: rstcommon.rst

     It's the current trick for brevity and compatibility with both Github and
     rst2html.py, considering that Github cannot highlight Brownie in
     RST files anyway and it does not include files.
     This way interpreted text is displayed with monospaced font in Github
     and it's displayed an Brownie code in both rst2html.py
     (note ".. default-role:: Brownie" above) and `brownie rst2html`.

     For files that are user manual and consist of stuff like cmdline
     option description, use 'code' as a **real** default role:

     .. include:: rstcommon.rst
     .. default-role:: code

.. define language roles explicitly (for compatibility with rst2html.py):

.. role:: brownie(code)
   :language: brownie

.. default-role:: brownie

.. role:: c(code)
   :language: c

.. role:: cpp(code)
   :language: cpp

.. role:: yaml(code)
   :language: yaml

.. role:: python(code)
   :language: python

.. role:: java(code)
   :language: java

.. role:: csharp(code)
   :language: csharp

.. role:: cmd(code)

.. role:: program(code)

.. role:: option(code)

