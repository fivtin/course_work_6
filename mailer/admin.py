from django.contrib import admin

from mailer.models import Client, Message, Newsletter, Attempt


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'fio', 'info', 'owner', )
    list_filter = ('owner', )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'body', 'owner', )
    list_filter = ('owner', )


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start', 'finish', 'frequency', 'status', 'message', 'is_block', 'owner', )
    list_filter = ('status', 'frequency', 'is_block', 'owner', )
    search_fields = ('title', 'message', )


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'newsletter', 'attempt_time', 'success', 'response', )
    list_filter = ('newsletter', 'success', )
