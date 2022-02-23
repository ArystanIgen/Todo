# Standard Library
import logging
from typing import Optional

from notifiers import get_notifier
from notifiers.core import Response

from todo import settings

logger = logging.getLogger(__name__)


class EmailSender:

    def __init__(self) -> None:  # type: ignore
        self.notifier = get_notifier('email')

    def send(self, email: str, subject: str, message: str) -> None:  # pragma: no cover
        options = dict(
            from_=settings.EMAIL_HOST_USER,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_HOST,
            tls=True,
            ssl=True,
            to=email,
            subject=subject,
            message=message,
            html=False,
        )
        response: Response = self.notifier.notify(**options)
        if response.status == 'Success':
            logger.info(f"Sent successfully! {options['to']=}")
        else:
            logger.error(f"{response.errors=} {response.response=} {response.data=}  {response.provider}")
