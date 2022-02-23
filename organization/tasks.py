import logging

from celery import shared_task

from organization.send_email import EmailSender

logger = logging.getLogger(__name__)


@shared_task(name="notify_task")
def notify_task(email: str, name: str):
    mail_subject = f"Deadline to {name}"
    message = f"One hour left before the deadline of the project {name}"
    logger.info(f"Sending mail to {email}")
    email_sender = EmailSender()

    email_sender.send(
        subject=mail_subject,
        message=message,
        email=email
    )
