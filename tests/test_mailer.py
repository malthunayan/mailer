import pathlib
from typing import Any

import pytest
import toml

from mailer import __version__


@pytest.fixture
def base_dir() -> pathlib.Path:
    return pathlib.Path(__file__).parents[1].expanduser().resolve()


@pytest.fixture
def metadata(base_dir: pathlib.Path) -> dict[str, Any]:
    pyproject = base_dir / "pyproject.toml"
    config = toml.loads(pyproject.read_text())
    return config["tool"]["poetry"]


def test_version(metadata: dict[str, Any]) -> None:
    version = metadata["version"]
    assert __version__ == version, "Versions do not match"
