from django.contrib import admin
from . import models


@admin.register(models.Mailing)
class ModelMailing(admin.ModelAdmin):
    list_display = ('start', 'finish', 'type', 'message')
    list_filter = ('start', 'finish', 'type')
    search_fields = ('start', 'finish', 'type')


@admin.register(models.Client)
class ModelClient(admin.ModelAdmin):
    list_display = ('phone', 'utc')
    search_fields = ('phone', 'utc', 'code', 'teg')


@admin.register(models.Message)
class ModelMessage(admin.ModelAdmin):
    list_display = ('date', 'delivered', 'mailing', 'client')
    list_filter = ('date', 'delivered', 'mailing', 'client')
    search_fields = ('date', 'delivered', 'mailing', 'client')
