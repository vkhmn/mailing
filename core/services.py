from datetime import datetime

import requests
from enum import Enum

from django.core.exceptions import ValidationError
from django.db.models import Q, QuerySet
from django.utils import timezone

from config.settings import API_KEY
from core.models import Mailing, Client, Message, Status


class CreateMessages:
    @classmethod
    def _find_clients(cls, mailing_id: str) -> list[str]:
        (code_id, tag_id), *_ = Mailing.objects.select_related(
            'filter').filter(pk=mailing_id).values_list('filter__code', 'filter__tag')

        return Client.objects.filter(
            Q(code_id=code_id) | Q(tag_id=tag_id)
        ).values_list('pk', flat=True)

    @classmethod
    def _create_messages(cls, mailing_id: str, client_ids: list[str]) -> None:
        messages = []
        for client_id in client_ids:
            message = Message(client_id=client_id, mailing_id=mailing_id)
            try:
                message.full_clean()
            except ValidationError as e:
                print(e)
            else:
                messages.append(message)

        Message.objects.bulk_create(messages)

    @classmethod
    def execute(cls, mailing_id: str) -> None:
        cls._create_messages(
            mailing_id=mailing_id,
            client_ids=cls._find_clients(mailing_id)
        )


class ChangeMessageStatusSend:
    @classmethod
    def execute(cls, message_id: str) -> None:
        message = Message.objects.get(pk=message_id)
        message.status = Status.SEND
        message.save()


class GetMessageInfo:
    @classmethod
    def execute(cls, mailing_id: str) -> QuerySet:
        return Message.objects.select_related('client', 'mailing').filter(
            mailing_id=mailing_id, status=Status.CREATE).values_list(
            'pk', 'client__phone', 'mailing__message_text')


class TaskStatus(Enum):
    WAITING = 0
    STARTED = 1
    ENDED = 2


class GetMailingStatus:
    @classmethod
    def execute(cls, mailing_id: str) -> TaskStatus:
        mailing = Mailing.objects.get(pk=mailing_id)
        current_date = datetime.now(tz=timezone.get_current_timezone())
        if current_date >= mailing.time_end:
            return TaskStatus.ENDED

        if current_date < mailing.time_start:
            return TaskStatus.WAITING

        return TaskStatus.STARTED


class SendMessage:
    @classmethod
    def execute(cls, message_id: str, phone: str, text: str) -> int:
        url = f"https://probe.fbrq.cloud/v1/send/{message_id}"
        data = {
            "id": int(message_id),
            "phone": int(phone),
            "text": text,
        }
        headers = {
            "Content-type": "application/json",
            "Accept": "text/plain",
            "Authorization": f"Bearer {API_KEY}",
        }
        return requests.post(url, json=data, headers=headers,).status_code
