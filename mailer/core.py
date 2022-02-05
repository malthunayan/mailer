import copy
import csv
import pathlib
import smtplib
import ssl
from collections.abc import Iterable, Iterator
from email.message import EmailMessage, Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from mailer.models import EmailSender


def get_message(
    content: pathlib.Path,
    html_content: pathlib.Path | None = None,
    subject: str | None = None,
    sender: str | None = None,
) -> Message:
    msg: Message
    if html_content:
        msg = MIMEMultipart("alternative")
        msg.attach(MIMEText(content.read_text(encoding="utf-8"), "plain"))
        msg.attach(MIMEText(html_content.read_text(encoding="utf-8"), "html"))
    else:
        msg = EmailMessage()
        msg.set_content(content.read_text(encoding="utf-8"))

    if subject:
        msg["Subject"] = subject

    if sender:
        msg["From"] = sender

    return msg


def get_recipients(recipients: pathlib.Path) -> Iterator[str]:
    with recipients.open(mode="r", newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            yield row[0]


def send_mail(
    recipients: Iterable[str] | str,
    msg: Message,
    sender: EmailSender,
    debuglevel: int = 0,
) -> None:
    if isinstance(recipients, str):
        recipients = (recipients,)

    context = ssl.create_default_context()
    with smtplib.SMTP(host=sender.host, port=sender.port) as mailer:
        mailer.set_debuglevel(debuglevel=debuglevel)
        mailer.starttls(context=context)
        mailer.login(user=sender.addr, password=sender.password)

        for recipient in recipients:
            copied = copy.deepcopy(msg)
            copied["To"] = recipient
            mailer.send_message(
                msg=copied, from_addr=sender.name, to_addrs=recipient
            )
