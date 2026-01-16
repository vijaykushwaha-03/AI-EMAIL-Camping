from django.contrib import admin
from .models import Campaign, EmailLog


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'status', 'sent_count', 'open_rate', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'subject']
    readonly_fields = ['id', 'sent_count', 'open_count', 'click_count', 'created_at', 'updated_at']
    filter_horizontal = ['recipients']
    ordering = ['-created_at']
    
    def open_rate(self, obj):
        return f"{obj.open_rate}%"
    open_rate.short_description = 'Open Rate'


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['campaign', 'contact', 'status', 'sent_at', 'opened_at']
    list_filter = ['status', 'sent_at']
    search_fields = ['contact__email', 'campaign__name']
    readonly_fields = ['id', 'sent_at']
    ordering = ['-sent_at']
