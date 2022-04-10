# Register your models here.
from django.contrib import admin

from .models import QA


@admin.register(QA)
class QAAdmin(admin.ModelAdmin):
    """Admin View for QA"""

    list_display = ("name", "email")
    readonly_fields = ("name", "email", "message")
    search_fields = ("name", "email")
