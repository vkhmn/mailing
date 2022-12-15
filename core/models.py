from django.db import models


class Code(models.Model):
    value = models.IntegerField(
        'Код оператора',
        unique=True,
    )

    def __str__(self):
        return f'{self.value}'


class Tag(models.Model):
    value = models.CharField(
        'Тег',
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return f'{self.value}'


class Filter(models.Model):
    code = models.ForeignKey(
        Code,
        on_delete=models.CASCADE,
        verbose_name='Код оператора',
        blank=True,
        null=True,
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег',
        blank=True,
        null=True,
    )


class Mailing(models.Model):
    """
    Сущность "рассылка" имеет атрибуты:
        •уникальный id рассылки
        •дата и время запуска рассылки
        •текст сообщения для доставки клиенту
        •фильтр свойств клиентов, на которых должна быть произведена рассылка
         (код мобильного оператора, тег)
        •дата и время окончания рассылки: если по каким-то причинам не успели
         разослать все сообщения - никакие сообщения клиентам после этого
         времени доставляться не должны
    """

    time_start = models.DateTimeField(
        'Дата и время запуска рассылки',
    )
    message_text = models.CharField(
        'Текст сообщения для доставки клиенту',
        max_length=200,
    )
    filter = models.ForeignKey(
        Filter,
        on_delete=models.CASCADE,
        verbose_name='Фильтр свойств клиентов',
    )
    time_end = models.DateTimeField(
        'Дата и время окончания рассылки',
    )


class Client(models.Model):
    """
    Сущность "клиент" имеет атрибуты:
        •уникальный id клиента
        •номер телефона клиента в формате 7XXXXXXXXXX (X - цифра от 0 до 9)
        •код мобильного оператора
        •тег (произвольная метка)
        •часовой пояс
    """
    phone = models.IntegerField(
        'Номер телефона',
        unique=True,
    )  # Add phone validator
    code = models.ForeignKey(
        Code,
        on_delete=models.CASCADE,
        verbose_name='Код мобильного оператора',
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег',
        blank=True,
        null=True,
    )
    time_zone = models.IntegerField(
        'Часовой пояс',
        default=0
    )

    def __str__(self):
        return f'{self.phone}'


class Status(models.TextChoices):
    """ Статус отправки."""

    CREATE = 'cr', 'Create'
    SEND = 'sn', 'Send'


class Message(models.Model):
    """
    Сущность "сообщение" имеет атрибуты:
        •уникальный id сообщения
        •дата и время создания (отправки)
        •статус отправки
        •id рассылки, в рамках которой было отправлено сообщение
        •id клиента, которому отправили
    """
    time_update = models.DateTimeField(
        'Дата и время создания (отправки)',
        auto_now=True,
    )
    status = models.CharField(
        'Статус отправки',
        choices=Status.choices,
        default=Status.CREATE,
        max_length=2,
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name='Рассылка',
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Клиент',
    )

    class Meta:
        unique_together = (('mailing', 'client'),)
