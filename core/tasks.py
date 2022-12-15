from config.celery import app
from core.services import (
    GetMessageInfo, ChangeMessageStatusSend, GetMailingStatus, TaskStatus,
    SendMessage
)


@app.task(
    bind=True,
    autoretry_for=(Exception, ),
    default_retry_delay=10 * 60,
    max_retries=None
)
def send_message_task(self, mailing_id: str) -> None:
    if not (GetMailingStatus.execute(mailing_id) == TaskStatus.STARTED):
        return None

    for message_id, phone, text in GetMessageInfo.execute(mailing_id):
        status_code = SendMessage.execute(message_id, phone, text)
        if status_code == 200:
            ChangeMessageStatusSend.execute(message_id=message_id)
        else:
            self.retry()
