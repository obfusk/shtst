#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : shtst
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2021-02-24
#
# Copyright   : Copyright (C) 2021  Felix C. Stegerman
# Version     : v0.1.0
# License     : GPLv3+
#
# --                                                            ; }}}1

import os, re, subprocess
from collections import namedtuple

import click

__version__ = "0.1.0"
name        = "shtst"

Spec = namedtuple("Spec", "cmd stdin stdout stderr exit lineno".split())

# TODO
@click.command(help = "simple cli testing")
@click.option("--shell", metavar = "PATH",
              help = "Shell program.  [default: /bin/sh]")
@click.argument("tests", nargs = -1, type = click.Path(exists = True),
                metavar = "[TESTFILES|TESTDIRS]")
@click.version_option(__version__)
@click.pass_context
def cli(ctx, tests, shell):                                     # {{{1
  passed, failed, total = 0, 0, 0
  for f in files(tests):
    for i, s in enumerate(parse(f)):
      total += 1
      err = tuple(run(s, shell))
      res = "Failed" if err else "OK"
      click.echo(":{}:{}: [{}]".format(f, i+1, res))
      if err:
        failed += 1
        click.echo("Command (at line {}):\n{}".format(s.lineno, s.cmd))
        click.echo("".join(err))
      else:
        passed += 1
  click.echo(
    "\n         Test Cases  Total\n" +
      " Passed  {:<10}  {}\n".format(passed, passed) +        #  FIXME
      " Failed  {:<10}  {}\n".format(failed, failed) +        #  FIXME
      " Total   {:<10}  {}"  .format(total , total )          #  FIXME
  )
  if failed: ctx.exit(1)
                                                                # }}}1

def run(s, shell = None):                                       # {{{1
  args = s.cmd if shell is None else [shell, "-c", s.cmd]
  p = subprocess.run(args, shell = shell is None, text = True,
                     input = s.stdin, capture_output = True)
  if not match(p.stdout, s.stdout):
    yield "Expected stdout:\n{}\nGot stdout:\n{}" \
          .format(show(s.stdout), p.stdout)
  if not match(p.stderr, s.stderr):
    yield "Expected stderr:\n{}\nGot stderr:\n{}" \
          .format(show(s.stderr), p.stderr)
  eok = p.returncode != int(s.exit[1:]) if s.exit.startswith("!") \
          else p.returncode == int(s.exit)
  if not eok:
    yield "Expected exit code:\n{}\nGot exit code:\n{}" \
          .format(s.exit, p.returncode)
                                                                # }}}1

def match(got, exp):
  if exp is None: return True
  if isinstance(exp, re.Pattern): return exp.search(got) is not None
  return got == exp

def show(s):
  if isinstance(s, re.Pattern):
    opts = ""
    if s.flags & re.I: opts += "i"
    if s.flags & re.M: opts += "m"
    if s.flags & re.S: opts += "s"
    return "/{}/{}".format(s.pattern, opts)
  return s

def regex(s):
  flags = 0
  pat, opts = s.split("/")[1:]
  if "i" in opts: flags |= re.I
  if "m" in opts: flags |= re.M
  if "s" in opts: flags |= re.S
  return re.compile(pat, flags)

# TODO
def parse(f):                                                   # {{{1
  def gobble(lines, j, l):
    s = ""
    while j < l:
      line = lines[j]
      if not line.strip() or line[0] in "#$?<>": break
      s += line[1:] if line.startswith("|") else line
      j += 1
    return s, j-1
  cmd, stdin, stderr, stdout, exit, lineno = \
    None, "", None, None, "0", None
  with open(f) as fh:
    lines = tuple(fh)
    i, l = 0, len(lines)
    while i < l:
      line = lines[i]
      if line.startswith("#") or not line.strip():
        pass
      elif line.startswith("$"):
        if cmd: yield Spec(cmd, stdin, stdout, stderr, exit, lineno)
        cmd, stdout, stderr, exit, lineno = \
          line[1:].strip(), None, None, "0", i+1
      elif line.startswith("?"):
        exit = line[1:].strip()
      elif line.startswith(">="):
        exit = line[2:].strip()
      elif line.startswith("<"):
        stdin, i = gobble(lines, i+1, l)
      elif line.startswith(">2"):
        if "/" in line:
          stderr = regex(line[2:].strip())
        else:
          stderr, i = gobble(lines, i+1, l)
      elif line.startswith(">"):
        if "/" in line:
          stdout = regex(line[1:].strip())
        else:
          stdout, i = gobble(lines, i+1, l)
      else:
        raise RuntimeError("Parse Error (file: {}, line: {})"
                           .format(f, i+1))                   #  FIXME
      i += 1
    if cmd: yield Spec(cmd, stdin, stdout, stderr, exit, lineno)
                                                                # }}}1

def files(ts):                                                  # {{{1
  for t in ts:
    if os.path.isdir(t):
      for fn in sorted(os.listdir(t)):
        fp = os.path.join(t, fn)
        if os.path.isdir(fp):
          for x in files([fp]):
            yield x
        elif fn.endswith(".test"):
          yield fp
    else:
      yield t
                                                                # }}}1

def main():
  cli(prog_name = name)

if __name__ == "__main__":
  main()

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
