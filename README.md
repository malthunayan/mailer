# Mailer

Send bulk email out to recipients.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Authors](#authors)

## Prerequisites

- [poetry](https://python-poetry.org/) 1.0.0+
- [Python](https://www.python.org/) 3.10+
- [pipx](https://pipxproject.github.io/pipx/) 0.15.5+ - optional dependency

## Installation

Follow the steps below to install project dependencies, build the project, and install it globally:

### Build (Bash/Zsh/Fish)

```bash
$ git clone <repo-url>
...
$ cd path/to/repo
$ poetry build
...
$ ls
dist mailer tests pyproject.toml README.md ...
$ ls dist/
mailer-0.1.0-py3-none-any.whl mailer-0.1.0.tar.gz
```

The `mailer` command will be available globally after following the steps below. To change the command name, change the variable name `mailer` in the `pyproject.toml` file, under `[tool.poetry.scripts]`, to something else.

**Important:** Check the [environment variables](#environment-variables) section to properly set up your environment for usage post building/installation.

#### pipx

```bash
$ pipx install --python python3.9 dist/mailer-0.1.0-py3-none-any.whl
...
```

**Note:** the Python and project versions can change, so `--python python3.11 dist/mailer-0.1.0-py3-none-any.whl` would work too if a different version of Python is installed on your system, or the project version is different.

#### pip (not recommended)

This is not recommended, because this will clutter the global pip dependencies installed.

```bash
$ pip install --user dist/mailer-0.1.0-py3-none-any.whl
...
```

## Authors

- [Mohammad Al-Thunayan](https://github.com/malthunayan)
