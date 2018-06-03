# pysetenv

[![PyPi version][pypi-image]][pypi-link]
[![Travis build status][travis-image]][travis-link]
[![Appveyor build status][appveyor-image]][appveyor-link]
[![Coverage status][codecov-image]][codecov-link]

**pysetenv** is a simple Python-based program to allow users to set environment
variables before executing a command. While it's cross-platform, it's primarily
designed to be used on Windows, where `cmd.exe` makes this considerably more
difficult than on POSIX systems.

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
