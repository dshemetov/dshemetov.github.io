---
title: "Python Project Structures"
date: 2022-09-02T17:29:37-07:00
draft: false
toc: true
tags: [
    "python"
]
---

Updated on: 2023-07-24.

Python project structures are confusing. Let's make them less so.

## Terminology

First, a few standard Python terminology definitions:

- a **module** is a single Python script,
- a **package** is a collection of modules[^1].

A project may be an application or a library:

- an **application** is a program that is meant to be deployed, such as a script for numerical calculations, a server, or a Discord bot,
- a **library** is a package that will be imported by other libraries or applications.

## Project Structures

There are a few common, recommended Python project structures[^2]. This is the one I prefer:

```sh
# A Simpler "src-layout" Structure
project_root/
    docs/
        conf.py
        index.md
    package/
        __init__.py
        subpackageA/
            __init__.py
            moduleA.py
        module.py
    tests/
        __init__.py
        test_module.py
    runner.py
    README.md
    LICENSE
    pyproject.toml
```

It separates tests from the package code and removes the unnecessary `src` folder.

- The `runner.py` script is the entry point for the application, such as a CLI (if you're building a library, you can omit this file).
- The `package` folder is the package that will be imported by other libraries or applications.
- The `tests` folder contains unit tests for the package.
- The `docs` folder contains documentation for the package.

The application is run with `python runner.py` from the top-level directory.

## Imports

Imports in each file can be handled as follows:

```py
# absolute import in runner.py
from package import module

# absolute import in package/module.py
from package.subpackageA import moduleA
# relative import in package/module.py
from .subpackageA import moduleA

# absolute import in package/subpackageA/moduleA.py
from package import module
# relative import in package/subpackageA/moduleA.py
from .. import module

# absolute import in tests/test_module.py
from package import module
from package.subpackageA import moduleA
```

Note that scripts can't import relative to each other, so you can't do `from . import module` in `runner.py` (this is because the `__name__` variable for `runner.py` is `__main__` when run as `python runner.py` and therefore Python can't do module name manipulation, see more [here](https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time)).

If you run `python runner.py` from the top-level directory, the `project_root` will be in your `PYTHONPATH` environment variable, so you can import `package` and its submodules from anywhere in the project.
If you run `python package/module.py` from the top-level directory, you will get an error because `PYTHONPATH` will not contain `project_root`.
You can test this by showing the Python path in `runner.py` and `package/module.py` (via the [`sys.path` variable](https://docs.python.org/3/library/sys.html?highlight=sys%20path#sys.path)):

```py
# runner.py
import sys
print(sys.path)

# package/module.py
import sys
print(sys.path)

# output of `python runner.py`:
['/path/to/project_root', ...]

# output of `python package/module.py`:
['/path/to/project_root/package', ...]
```

Alternatively, you can run a package script from the top-level directory by using `-m` flag (see more on the [-m flag here](https://docs.python.org/3/using/cmdline.html#cmdoption-m)):

```sh
python -m package.module
```

For testing, `pytest .` should work from any directory[^3].

## A Word On `pyproject.toml`

The Python community appears to have organized around using `pyproject.toml` to specify

- package metadata
- build dependencies and environments
- tool configurations

See [PEP-518](https://peps.python.org/pep-0518/) and [PEP-621](https://peps.python.org/pep-0621/) for official specifications.

This unifies many configuration files, such as

- `.pylintrc`
- `setup.py`
- `setup.cfg`
- `requirements.txt`

Many other tools, such as `black` and `pytest` already support setting their configurations in `pyproject.toml` as well.

For a little history and an introduction to the file, see [Brett Cannon's blog post](https://snarky.ca/what-the-heck-is-pyproject-toml/) (Brett is one of the authors of PEP-518 and related PEPs).

Here is a sample `pyproject.toml` for a package that uses the `setuptools` backend.

```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "package_name"
version = "0.1.0"
description = "Useful utilities"
readme = "README.md"
requires-python = ">=3.10"
authors = [
  {email = ""},
  {name = ""}
]
classifiers = [
  "Development Status :: 4 - Beta",
  "Programming Language :: Python"
]
dependencies = [
  "numpy"
]

[project.urls]
repository = ""

[tool.setuptools]
# To specify specific folders or modules to install
py-modules = ["package_folder"]

[tool.black]
target-version = ['py310']
include = '\.py'

[tool.pytest.ini_options]
minversion = "6.0"
addopts = "--doctest-modules --doctest-continue-on-failure"

[tool.pylint.'FORMAT']
max-line-length=100
```

## Footnotes

[^1]: [These definitions are 90% true](https://docs.python.org/3/reference/import.html#packages).
    Package is an [overloaded term in Python](https://stackoverflow.com/a/54599368/4784655).
[^2]: This structure is recommended by the popular [Hitchhiker's Guide to Python](https://docs.python-guide.org/writing/structure/).
    It is also default for [`poetry` projects](https://github.com/python-poetry/poetry), a common Python workflow tool.
[^3]: `pytest` will find your project root by traversing up the directory hierarchy, see [more here](https://docs.pytest.org/en/7.1.x/explanation/pythonpath.html#test-modules-conftest-py-files-inside-packages)
