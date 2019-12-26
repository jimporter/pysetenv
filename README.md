# pysetenv

[![PyPi version][pypi-image]][pypi-link]
[![Travis build status][travis-image]][travis-link]
[![Appveyor build status][appveyor-image]][appveyor-link]
[![Coverage status][codecov-image]][codecov-link]

**pysetenv** is a simple Python-based program to allow users to set environment
variables before executing a command, similar to the POSIX [`env`][env] command.

## Why?

pysetenv is designed as a support package to help authors of other Python
packages create command-line strings like you'd expect from `sh` or the `env`
command. Generally, pysetenv will only be installed on Windows systems, with
POSIX systems using `sh` or `env`. For example, in your `setup.py`, you would
write:

```python
setup(
    # ...
    install_requires=['pysetenv;platform_system=="Windows"'],
)
```

Then somewhere in your code, you could call pysetenv:

```python
subprocess.call(['pysetenv', ...])
```

## Command-line reference

Usage: `pysetenv [OPTION]... [NAME=VALUE]... [--] [COMMAND [ARG]...]`

pysetenv supports a subset of common options available to various
implementations of `env`. It executes `COMMAND` with any supplied arguments
(`ARG`) after modifying the environment as specified by the previous arguments.
Any arguments of the form `NAME=VALUE` will set an environment variable `NAME`
to the value of `VALUE`. If `COMMAND` is not specified, pysetenv will print the
resulting environment instead.

In addition, the following options are supported:

* `-i`: Ignore any environment variables inherited by this process
* `-u NAME`: Unset the environment variable `NAME`
* `-h`, `--help`: Show a help message and exit
* `--version`: Show the current version and exit

As an extension to the `env` command, the options above and the variable
definitions can be separated from the section for defining the command to run
with `--`:

```sh
pysetenv -uFOO BAR=value -- echo hello
```

## License

This project is licensed under the [BSD 3-clause license](LICENSE).

[pypi-image]: https://img.shields.io/pypi/v/pysetenv.svg
[pypi-link]: https://pypi.python.org/pypi/pysetenv
[travis-image]: https://travis-ci.org/jimporter/pysetenv.svg?branch=master
[travis-link]: https://travis-ci.org/jimporter/pysetenv
[appveyor-image]: https://ci.appveyor.com/api/projects/status/63t32hh6df519788/branch/master?svg=true
[appveyor-link]: https://ci.appveyor.com/project/jimporter/pysetenv/branch/master
[codecov-image]: https://codecov.io/gh/jimporter/pysetenv/branch/master/graph/badge.svg
[codecov-link]: https://codecov.io/gh/jimporter/pysetenv
[env]: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/env.html
