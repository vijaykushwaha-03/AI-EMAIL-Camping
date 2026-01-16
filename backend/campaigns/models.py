import uuid
from django.db import models
from contacts.models import Contact


class Campaign(models.Model):
    """Campaign model for email campaigns"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=500)
    content = models.TextField(blank=True, default='')  # HTML content
    cc_email = models.EmailField(null=True, blank=True, help_text="CC email address (receives a copy of EVERY email)")
    bcc_email = models.EmailField(null=True, blank=True, help_text="BCC email address (receives a copy of EVERY email)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_count = models.IntegerField(default=0)
    open_count = models.IntegerField(default=0)
    click_count = models.IntegerField(default=0)
    recipients = models.ManyToManyField(Contact, blank=True, related_name='campaigns')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.status})"
    
    @property
    def open_rate(self):
        if self.sent_count > 0:
            return round(self.open_count / self.sent_count * 100, 1)
        return 0.0
    
    @property
    def click_rate(self):
        if self.sent_count > 0:
            return round(self.click_count / self.sent_count * 100, 1)
        return 0.0


class EmailLog(models.Model):
    """Log for tracking individual email sends"""
    
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('opened', 'Opened'),
        ('clicked', 'Clicked'),
        ('bounced', 'Bounced'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='email_logs')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='email_logs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    sent_at = models.DateTimeField(auto_now_add=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.campaign.name} → {self.contact.email} ({self.status})"
