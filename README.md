![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_new-logo_horizontal_rgb_small.png)

# autohooks-plugin-mypy

[![GitHub releases](https://img.shields.io/github/release/greenbone/autohooks-plugin-mypy.svg)](https://github.com/greenbone/autohooks-plugin-mypy/releases)
[![PyPI release](https://img.shields.io/pypi/v/autohooks-plugin-mypy.svg)](https://pypi.org/project/autohooks-plugin-mypy/)
[![code test coverage](https://codecov.io/gh/greenbone/autohooks-plugin-mypy/branch/main/graph/badge.svg)](https://codecov.io/gh/greenbone/autohooks-plugin-mypy)
[![Build and test](https://github.com/greenbone/autohooks-plugin-mypy/actions/workflows/ci-python.yml/badge.svg)](https://github.com/greenbone/autohooks-plugin-mypy/actions/workflows/ci-python.yml)

An [autohooks](https://github.com/greenbone/autohooks) plugin for python code
static typing check via [mypy](https://github.com/python/mypy).

## Installation

### Install using pip

You can install the latest stable release of autohooks-plugin-mypy from the
Python Package Index using [pip](https://pip.pypa.io/):

    python3 -m pip install autohooks-plugin-mypy

### Install using poetry

It is highly encouraged to use [poetry](https://python-poetry.org) for
maintaining your project's dependencies. Normally autohooks-plugin-mypy is
installed as a development dependency.

    poetry install

## Usage

To activate the mypy autohooks plugin please add the following setting to your
*pyproject.toml* file.

```toml
[tool.autohooks]
pre-commit = ["autohooks.plugins.mypy"]
```

By default, autohooks plugin mypy checks all files with a *.py* ending. If
only files in a sub-directory or files with different endings should be
formatted, just add the following setting:

```toml
[tool.autohooks]
pre-commit = ["autohooks.plugins.mypy"]

[tool.autohooks.plugins.mypy]
include = ['foo/*.py', '*.foo']
```

By default, autohooks plugin mypy executes mypy without any arguments.
To change specific settings or to define a mypy config file the following plugin configuration can be used:

```toml
[tool.autohooks]
pre-commit = ["autohooks.plugins.mypy"]

[tool.autohooks.plugins.mypy]
arguments = ["--ignore-missing-imports", "--config-file=/path/to/.mypy.ini"]
```

## Maintainer

This project is maintained by [Greenbone AG](https://www.greenbone.net/).

## Contributing

Your contributions are highly appreciated. Please
[create a pull request](https://github.com/greenbone/autohooks-plugin-mypy/pulls)
on GitHub. Bigger changes need to be discussed with the development team via the
[issues section at GitHub](https://github.com/greenbone/autohooks-plugin-mypy/issues)
first.

## License

Copyright (C) 2021 [Vincent Texier](https://gitlab.com/VictorIndiaTango).
Copyright (C) 2023 [Greenbone AG](https://www.greenbone.net/)

Licensed under the [GNU General Public License v3.0 or later](LICENSE).
