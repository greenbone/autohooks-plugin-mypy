# autohooks-plugin-mypy

An [autohooks](https://github.com/greenbone/autohooks) plugin for python code
static typing check via [mypy](https://github.com/python/mypy).

## Installation

### Install using pip

You can install the latest stable release of autohooks-plugin-mypy from the
Python Package Index using [pip](https://pip.pypa.io/):

    pip install autohooks-plugin-mypy

Note the `pip` refers to the Python 3 package manager. In an environment where
Python 2 is also available the correct command may be `pip3`.

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

This project is maintained by [Vincent Texier](https://gitlab.com/VictorIndiaTango).

## Contributing

Your contributions are highly appreciated. Please
[create a merge request](https://gitlab.com/VictorIndiaTango/autohooks-plugin-mypy/-/merge_requests)
on GitHub. Bigger changes need to be discussed with the development team via the
[issues section at Gitlab](https://gitlab.com/VictorIndiaTango/autohooks-plugin-mypy/-/issues)
first.

## License

Copyright (C) 2021 [Vincent Texier](https://gitlab.com/VictorIndiaTango).

Licensed under the [GNU General Public License v3.0 or later](LICENSE).
