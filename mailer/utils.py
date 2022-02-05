from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

from mailer.exceptions import MailerError


_T = TypeVar("_T")
_P = ParamSpec("_P")


def safe_exit(func: Callable[_P, _T]) -> Callable[_P, _T]:
    @wraps(func)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        try:
            return func(*args, **kwargs)
        except (KeyboardInterrupt, EOFError):
            print()
            raise SystemExit(1)
        except MailerError as exc:
            raise SystemExit(f"Error: {exc}")

    return wrapper
