from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Mailing, Client
from core.services import CreateMessages, TaskStatus, GetMailingStatus
from core.tasks import send_message_task


@receiver(post_save, sender=Mailing)
def create_mailing(sender, instance: Mailing, **kwargs) -> None:
    CreateMessages.execute(instance.pk)

    status = GetMailingStatus.execute(mailing_id=instance.pk)
    if status == TaskStatus.WAITING:
        send_message_task.apply_async(
            (instance.id,), eta=instance.time_start
        )
    elif status == TaskStatus.STARTED:
        send_message_task.delay(instance.id)
