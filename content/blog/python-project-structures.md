---
title: "Python Project Structures"
date: 2022-09-02T17:29:37-07:00
draft: false
toc: true
tags: [
    "python"
]
---

Python project structures are confusing. Let's make them less so.

## Terminology

First, a few standard Python terminology definitions:

- a **module** is a single Python script,
- a **package** is a collection of modules.[^1]

A project may be an application or a library:

- an **application** is a program that is meant to be deployed, such as a simple script, a server, or a Discord bot,
- a **library** is a package that will be imported by other libraries or applications.

## Project Structures

There are a few recommended, [best-practice Python project structures](https://docs.python-guide.org/writing/structure/).

```sh
# A "src-layout" Structure
project_root/
    docs/
        conf.py
        index.md
    src/
        package/
            __init__.py
            module.py
    tests/
        __init__.py
        test_module.py
    README.md
    LICENSE
    pyproject.toml

# A Simpler "src-layout" with Tests In Package
project_root/
    docs/
        conf.py
        index.md
    package/
        __init__.py
        module.py
        tests/
            __init__.py
            test_module.py
    README.md
    LICENSE
    pyproject.toml

# A Simpler "src-layout" Structure
project_root/
    docs/
        conf.py
        index.md
    package/
        __init__.py
        module.py
    tests/
        __init__.py
        test_module.py
    README.md
    LICENSE
    pyproject.toml
```

My personal preference is option 3:

- in option 1, the extra `src` folder has never been necessary to me,
- in option 2, I don't think it's a good idea to include tests *inside your package folder*, because it introduces unnecessary bloat to users that aren't developers.

## Python Imports

Suppose that we go with option 3.

### Imports in Tests

How can we import functions from `module.py` into tests?
The following is good enough.

```py
# test_module.py
from package.module import module_func
```

If you use pytest, you can run `pytest .` in either in `project_root`, or in `project_root/tests` and the imports work just fine.
This is because `pytest` can find the project root by first discovering tests in subfolders, traversing up the directory hierarchy until it finds a directory without tests, and appends that to Python path.
See [here for more](https://docs.pytest.org/en/7.1.x/explanation/pythonpath.html#test-modules-conftest-py-files-inside-packages) and [here if you want to modify `pytest`'s Python path](https://stackoverflow.com/a/50610630/4784655).

### Imports Between Subpackages

Now suppose you have a subpackage `utils`.
How can we import this into `package/module.py`?

```sh
project_root/
    docs/
        conf.py
        index.md
    package/
        __init__.py
        module.py
    utils/
        __init__.py
        tool.py
    tests/
        __init__.py
        test_module.py
    runner.py
    README.md
    LICENSE
    pyproject.toml
```

The same answer as before works, but under a few conditions.

```py
# module.py
from utils.tool import util_func
```

The main condition is that the file that eventually runs your code needs to be in the top-level directory, e.g. `python runner.py`.
What you *couldn't* do, is run this in `/project_root` dir

```sh
python package/module.py
```

because its [`sys.path` variable](https://docs.python.org/3/library/sys.html?highlight=sys%20path#sys.path) would not contain the `utils` package and you will get an error.

Instead you could use the `-m` flag to run as module

```sh
python -m package.module
```

(note the missing file extension and the directory slash replaced by a period).

Another option is to modify `sys.path` in `package/module.py` like this:

```py
# module.py
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

from utils.tool import util_func
```

Personally, these do not spark joy.
My solution so far has been:

- for applications, the executable script is a top-level script outside the packages
  - if you have submodules with code you want to execute, create a `runner.py` script that imports their code and executes it
- for libraries, don't worry about it (hasn't ever been an issue).

### But What About Relative Imports?

This is not very deep, but:

- relative imports won't fix the issues with directly executing submodules,
- relative imports won't let you import something that you can't import with an absolute import (I'm pretty sure, but I'd like to find a Guido quote for this or something).

So maybe just don't?

See the top answer [to understand relative imports and their limitations](https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time).

## A Word On `pyproject.toml`

The Python community appears to have organized around using `pyproject.toml` to specify

- package metadata
- build dependencies and environments
- tool configurations

See [PEP-518](https://peps.python.org/pep-0518/) and [PEP-621](https://peps.python.org/pep-0621/) for official specifications.

This deprecates many configuration files, such as

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
  "joblib",
  "more-itertools",
  "numpy"
]

[project.urls]
repository = ""

[tool.setuptools]
# To specify specific folders or modules to install
py-modules = ["package_folder"]

[tool.black]
line-length = 180
target-version = ['py310']
include = '\.py'

[tool.pytest.ini_options]
minversion = "6.0"
addopts = "--doctest-modules --doctest-continue-on-failure"

[tool.pylint.'FORMAT']
max-line-length=180
```

## References

- Many of my ideas came from this [Python-guide on project structure](https://docs.python-guide.org/writing/structure/).

## Footnotes

[^1]: [These are only 90% true, but that's good enough](https://docs.python.org/3/reference/import.html#packages).
    Package is an [overloaded term in Python](https://stackoverflow.com/a/54599368/4784655).
