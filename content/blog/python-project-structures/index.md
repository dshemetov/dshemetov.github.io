---
# Generated from the Obsidian vault by scripts/vault_export.py. Edit the note there.
title: An Opinionated Guide to Python Projects
date: 2022-09-02T17:29:37-07:00
toc: true
tags:
  - python
  - software
slug: python-projects
aliases:
  - /python-project-structures/
---

Updated on: 2026-10-18.

This post is meant to be an opinionated guide to setting up and developing a Python project. The goal is to give a paved path that avoids common snags.

## Let `uv` manage Python

Python project management has become drastically simpler with the introduction of [uv](https://github.com/astral-sh/uv) (which consolidated many tools and made everything way faster). There are a few main things it will handle for you: setting up a project structure, installing Python, and installing the dependencies.

Much of your use of `uv` can reduce down to simply using `uv run` to execute everything.

```sh
# Run a script
uv run file.py
# Run tests
uv run pytest
# Start a Python shell
uv run python
# Run a bash script with the Python environment active
uv run ./mybash.sh
```

(You can use `alias ur="uv run"` to type less, but I find I generally don't need it.)

This all works because `uv run X` will automatically:

- create a `.venv` directory with a bare virtual environment and ensure you have an isolated Python that matches your project's requirements (similar to calling `uv venv`)[^7]
- install your project dependencies in the `.venv` environment (similar to calling `uv sync`)
- execute `X` in an environment where the packages from `.venv` are available and so are the additional programs in `.venv/bin`

This takes care of all Python and environment management issues (as long as your project is configured correctly).[^6]

## Use `uv init` to get a standard project layout

If you're starting a brand new project, `uv init` will create the boilerplate for you, along with a template `pyproject.toml`.

```toml
[project]
name = "package"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
authors = [
    { name = "Dmitry Shemetov", email = "..." }
]
requires-python = ">=3.15"
dependencies = []

[project.scripts]
package = "package:main"

[build-system]
requires = ["uv_build>=0.12.17,<0.13.0"]
build-backend = "uv_build"
```

This is the layout the above command prepares:[^9]

```sh
.
├── pyproject.toml
├── README.md
└── src
    └── package
        └── __init__.py
```

With these contents:

```python
# __init__.py
def main() -> None:
    print("Hello from package!")
```

As your project develops, you will probably want to add:

- a `tests/` top-level directory with files like `test_module.py` which `pytest` will automatically collect and run
- a `docs/` directory for documentation
- a `LICENSE` file

## Use `main` as your program entry point

(If your project is a library and doesn't need an entry point, you can use `uv init --lib` or simply delete the `[project.scripts]` section in `pyproject.toml`.)

How do we actually call our program though? We need an entry point. The sample project above defines it in `[project.scripts]` in `pyproject.toml` to be the `main` function, so

```sh
❯ uv run package
Hello from package!
```

This is preferable to executing files directly with `uv run python script.py` or `uv run file.py` because the command doesn't depend on file paths (and relative imports can break when files are run directly).

Generally, it's handy to have some ways to customize your program's behaviors. This is where [`typer`](https://typer.tiangolo.com/) can help you to quickly make a CLI by taking much of the boilerplate out of the process of capturing arguments.

## Use absolute imports

When importing sibling modules into a module, you can either use relative or absolute imports. My preference is to stick to absolute imports, because this consistency makes repo-wide import searches comprehensive.

```python
# absolute import in package/module.py
from package.subpackageA import moduleA

# absolute import in package/subpackageA/moduleA.py
from package import module
```

If imports are giving you troubles, some helpful commands for debugging:

```sh
# Print the actual copy of the package imported.
uv run python -c 'import package; print(package.__file__)'
# Print the directories Python searches for imports, in order.
uv run python -c 'import sys; print(*sys.path, sep="\n")'
```

## Standard dependencies

Some useful tools I use in most projects:

- [`ruff` is the standard code formatter and linter](https://github.com/astral-sh/ruff)
- [`pytest` is the standard testing framework](https://docs.pytest.org/)
- [`typer` is a very handy CLI framework](https://typer.tiangolo.com/)

```toml
dependencies = [
    "typer>=0.27.3",
]

[dependency-groups]
dev = [
    "pytest>=9.1.1",
    "ruff>=0.17.1",
]
```

Along with my standard ruff settings:

```toml
[tool.ruff]
line-length = 120
lint.extend-select = [
    "I", # isort
    "NPY", # numpy
]
format.docstring-code-format = true
```

## Further reading

These are handy references if you ever need to go deeper:

- [Writing your pyproject.toml - Python Packaging User Guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
- [Working on projects | uv](https://docs.astral.sh/uv/guides/projects/)
- [Good Integration Practices - pytest documentation](https://docs.pytest.org/en/stable/explanation/goodpractices.html)
- [Modules - The Python Tutorial](https://docs.python.org/3/tutorial/modules.html), modules vs packages distinction and terminology
- [Dependency groups and uv run | Simon Willison’s TILs](https://til.simonwillison.net/uv/dependency-groups)

## Footnotes

[^6]: If you're working on an older Python project, `uv sync` might not work directly. You might need to do `uv init --bare` (to make sure you have a `pyproject.toml`), then `uv add -r requirements.txt` to install and record in `uv.lock`.

[^7]: If you're entering an existing project, `uv` will read either `.python-version` or `pyproject.toml` to understand which version of Python your project needs (or else default to something recent). You can also see which Pythons `uv` has installed on your system with `uv python list`.

[^9]: We just use `uv`'s default. The benefits of the `src/` layout over the "flat" layout are relatively minor - see [here](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).
