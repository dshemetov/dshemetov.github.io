+++
title = "Python Project Structures"
date = "2022-09-02T17:29:37-07:00"
toc = true
tags = [
    "python"
]
+++

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
    requirements.txt
    runner.py
    README.md
    LICENSE
    pyproject.toml
```

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

## Managing Pythons, Dependencies, and Environments

When it comes to Python management, I like to keep it simple.
I [use `pyenv`](https://github.com/pyenv/pyenv) to manage Python versions and `python -m venv venv` to create virtual environments in my project.
My standard `requirements.txt` file looks like this:

```txt
black
ruff
pytest
typer[all]
```

- [`black` is a code formatter](https://black.readthedocs.io/en/stable/),
- [`ruff` is a linter](https://beta.ruff.rs/docs/),
- [`pytest` is a testing framework](https://docs.pytest.org/),
- [`typer` is a CLI framework](https://typer.tiangolo.com/typer-cli/).

The modern place to store tool configuration settings is `pyproject.toml`. [Here](https://gist.github.com/dshemetov/30001cf62798c3b749cbb26bd977946b) is a sample `pyproject.toml` I use for my projects.
(See [here](https://snarky.ca/what-the-heck-is-pyproject-toml/) for an introductory blog post by Brett Cannon, one of the authors of [PEP-518](https://peps.python.org/pep-0518/) and [PEP-621](https://peps.python.org/pep-0621/).)

## Footnotes

[^1]:
    [These definitions are 90% true](https://docs.python.org/3/reference/import.html#packages).
    Package is an [overloaded term in Python](https://stackoverflow.com/a/54599368/4784655).

[^2]:
    This structure is recommended by the popular [Hitchhiker's Guide to Python](https://docs.python-guide.org/writing/structure/).
    It is also default for [`poetry` projects](https://github.com/python-poetry/poetry), a common Python workflow tool.

[^3]: `pytest` will find your project root by traversing up the directory hierarchy, see [more here](https://docs.pytest.org/en/7.1.x/explanation/pythonpath.html#test-modules-conftest-py-files-inside-packages)
