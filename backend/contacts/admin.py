from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'company', 'is_subscribed', 'created_at']
    list_filter = ['is_subscribed', 'created_at']
    search_fields = ['email', 'name', 'company']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
