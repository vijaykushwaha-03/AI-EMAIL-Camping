from rest_framework import serializers
from .models import Campaign, EmailLog


class CampaignSerializer(serializers.ModelSerializer):
    open_rate = serializers.FloatField(read_only=True)
    click_rate = serializers.FloatField(read_only=True)
    recipient_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Campaign
        fields = [
            'id', 'name', 'subject', 'content', 'status',
            'scheduled_at', 'sent_count', 'open_count', 'click_count',
            'open_rate', 'click_rate', 'recipient_count', 'created_at'
        ]
        read_only_fields = ['id', 'sent_count', 'open_count', 'click_count', 'created_at']
    
    def get_recipient_count(self, obj):
        return obj.recipients.count()


class CampaignCreateSerializer(serializers.ModelSerializer):
    recipient_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        write_only=True
    )
    
    class Meta:
        model = Campaign
        fields = ['name', 'subject', 'content', 'scheduled_at', 'recipient_ids']
    
    def create(self, validated_data):
        recipient_ids = validated_data.pop('recipient_ids', [])
        campaign = Campaign.objects.create(**validated_data)
        if recipient_ids:
            from contacts.models import Contact
            contacts = Contact.objects.filter(id__in=recipient_ids)
            campaign.recipients.set(contacts)
        return campaign


class EmailLogSerializer(serializers.ModelSerializer):
    contact_email = serializers.CharField(source='contact.email', read_only=True)
    
    class Meta:
        model = EmailLog
        fields = ['id', 'contact_email', 'status', 'sent_at', 'opened_at', 'clicked_at']
