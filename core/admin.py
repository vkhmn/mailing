from django.contrib import admin

from core.models import Message, Client, Mailing, Tag, Code, Filter


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    pass


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    pass
