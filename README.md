<!-- {{{1

    File        : README.md
    Maintainer  : Felix C. Stegerman <flx@obfusk.net>
    Date        : 2021-02-24

    Copyright   : Copyright (C) 2021  Felix C. Stegerman
    Version     : v0.1.1
    License     : GPLv3+

}}}1 -->

[![GitHub Release](https://img.shields.io/github/release/obfusk/shtst.svg?logo=github)](https://github.com/obfusk/shtst/releases)
[![PyPI Version](https://img.shields.io/pypi/v/shtst.svg)](https://pypi.python.org/pypi/shtst)
[![Python Versions](https://img.shields.io/pypi/pyversions/shtst.svg)](https://pypi.python.org/pypi/shtst)
[![CI](https://github.com/obfusk/shtst/workflows/CI/badge.svg)](https://github.com/obfusk/shtst/actions?query=workflow%3ACI)
[![GPLv3+](https://img.shields.io/badge/license-GPLv3+-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)

## shtst - simple cli testing

`shtst` is a command-line tool for testing command-line programs
against a simple specification of their expected output and exit code
given certain options and input.

It is inspired by (and similar to)
[shelltestrunner](https://github.com/simonmichael/shelltestrunner).

## Test Specification Format

```bash
# '#' starts a comment line; blank lines are ignored

# '$' starts a command line
$ true

# '?' specifies the expected return code [default: 0]
$ false
? 1

# '>' starts a stdout specification (which ends at the first line that
# is either blank or starts with a '#', '$', '?', '<', or '>')
$ echo foo
>
foo

# '<' starts an input specification (which ends the same way)
$ cat
<
foo
bar
>
foo
bar

# input from the previous command (if any) is reused if not specified
$ wc -l
2

# prefixing the input/output lines with '|' allows blank lines and
# other input/output that would otherwise end the specification (and
# lines that start with '|')
$ printf "foo\n\n<>\n"
>
|foo
|
|<>

# instead of literal lines of output, you can provide a regex
# (delimited by '/' and optionally followed by flags: 'i' for case
# insensitive, 'm' for multiline, and 's' for dotall) immediately
# after '>' or '>2'
$ printf "Line 1 foo\nLine 2 bar\nLine 3 baz\n"
> /^line 1.*^line 2/ims

# use '>2' instead of '>' to specify stderr instead of stdout
$ cat --oops
>2 /unrecognized option/
? 1

# use a '!' before the exit code to negate the test
$ echo 'does not return 42'
? !42

# no stdout/stderr specification means anything is accepted;
# explicitly use an empty specification if necessary
$ echo OK
>2
```

A test case always starts with a command line.  All input/output/exit
code specifications belong to the preceding command line.  With one
exception: you can specify input before the first command, which will
then be used for all subsequent commands until the next input
specification.

```bash
<
foo
bar
baz

$ cat
>
foo
bar
baz

$ wc -l
> 3
```

## Help

```bash
$ shtst --help
```

## Tab Completion

For Bash, add this to `~/.bashrc`:

```bash
eval "$(_SHTST_COMPLETE=source_bash shtst)"
```

For Zsh, add this to `~/.zshrc`:

```zsh
eval "$(_SHTST_COMPLETE=source_zsh shtst)"
```

For Fish, add this to `~/.config/fish/completions/shtst.fish`:

```fish
eval (env _SHTST_COMPLETE=source_fish shtst)
```

## Requirements

* Python >= 3.7 + click.

### Debian/Ubuntu

```bash
$ apt install python3-click
```

## Installing

### Using pip

```bash
$ pip install shtst
```

NB: depending on your system you may need to use e.g. `pip3 --user`
instead of just `pip`.

### From git

NB: this installs the latest development version, not the latest
release.

```bash
$ git clone https://github.com/obfusk/shtst.git
$ cd shtst
$ pip install -e .
```

NB: you may need to add e.g. `~/.local/bin` to your `$PATH` in order
to run `shtst`.

To update to the latest development version:

```bash
$ cd shtst
$ git pull --rebase
```

## License

[![GPLv3+](https://www.gnu.org/graphics/gplv3-127x51.png)](https://www.gnu.org/licenses/gpl-3.0.html)

<!-- vim: set tw=70 sw=2 sts=2 et fdm=marker : -->
