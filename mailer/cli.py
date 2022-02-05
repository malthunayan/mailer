import os
import pathlib
import textwrap
from argparse import ArgumentParser, Namespace
from email.policy import SMTP
from getpass import getpass
from typing import Sequence

from mailer.core import get_message, get_recipients, send_mail
from mailer.exceptions import MailerError
from mailer.models import EmailSender
from mailer.utils import safe_exit


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description=textwrap.dedent(
            """\
            Send bulk emails out to recipients from CSV file. The CSV file
            should contain only one column with no header, no empty rows, and
            all rows should be valid emails (no validation is done to ensure
            this). Use the '-o / --output' option to print the composed message
            to a FILE instead of actually sending it. A sender name is
            recommended to reduce the chances of being marked as spam. Sending
            only plain text also decreases the likelihood of being marked as
            spam by email providers."""
        )
    )

    # Arguments
    parser.add_argument("sender", help="sending email address (required)")
    parser.add_argument(
        "recipients",
        help="path to CSV file containing recipient email addresses (required)",
        type=pathlib.Path,
    )
    parser.add_argument(
        "content",
        help="path to text file containing email message body (required)",
        type=pathlib.Path,
    )
    parser.add_argument(
        "html_content",
        help="path to HTML file containing rich email message body",
        type=pathlib.Path,
        nargs="?",
    )

    # Options
    parser.add_argument(
        "-s", "--subject", help="email subject", dest="subject"
    )
    parser.add_argument(
        "-n", "--name", help="sending email name", dest="sender_name"
    )
    parser.add_argument("--host", help="SMTP host")
    parser.add_argument(
        "-p", "--port", help="SMTP port", dest="port", type=int
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        help=textwrap.dedent(
            """\
            print the composed message to FILE instead of sending the message
            to the SMTP server"""
        ),
        type=pathlib.Path,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        dest="debuglevel",
        help="Increase vebosity level",
    )

    return parser


def get_sender(
    addr: str,
    name: str | None = None,
    host: str | None = None,
    port: int | None = None,
) -> EmailSender:
    password = os.getenv("PASSWORD")
    if password is None:
        password = getpass("Password: ")

    try:
        return EmailSender(
            addr=addr, password=password, name=name, host=host, port=port
        )
    except TypeError as exc:
        raise MailerError(exc)


@safe_exit
def main(
    args: Sequence[str] | None = None, namespace: Namespace | None = None
) -> None:
    parser = get_parser()
    namespace = parser.parse_intermixed_args(args=args, namespace=namespace)

    sender = get_sender(
        addr=namespace.sender,
        name=namespace.sender_name,
        host=namespace.host,
        port=namespace.port,
    )
    recipients = get_recipients(namespace.recipients)
    msg = get_message(
        content=namespace.content,
        html_content=namespace.html_content,
        subject=namespace.subject,
        sender=sender.name,
    )

    output: pathlib.Path | None
    if output := namespace.output:
        msg["To"] = ", ".join(recipients)
        output.write_bytes(msg.as_bytes(policy=SMTP))
    else:
        send_mail(
            recipients=recipients,
            msg=msg,
            sender=sender,
            debuglevel=namespace.debuglevel,
        )


if __name__ == "__main__":
    main()
