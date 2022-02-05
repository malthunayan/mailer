from dataclasses import InitVar, dataclass, field


@dataclass
class EmailSender:
    addr: str
    password: str = field(repr=False)

    name: InitVar[str | None] = None

    host: InitVar[str | None] = None
    port: InitVar[int | None] = None

    def __post_init__(
        self, name: str | None, host: str | None, port: int | None
    ) -> None:
        self.host = host or self._get_host()
        self.port = port or 587
        self.name = f"{name} <{self.addr}>" if name else self.addr

    def _get_host(self) -> str:
        domain = self.addr.rsplit("@", maxsplit=1).pop()
        domain_name = domain.split(".", maxsplit=1).pop(0)

        if domain_name == "gmail":
            host = "smtp.gmail.com"
        elif domain_name == "yahoo":
            host = "smtp.mail.yahoo.com"
        elif domain_name in ("outlook", "live", "hotmail"):
            host = "smtp-mail.outlook.com"
        else:
            ctx = (
                f"could not dynamically determine SMTP host for '{self.addr}'"
            )
            raise TypeError(f"'host' is required ({ctx})")

        return host
