from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'email', 'name', 'company', 'tags', 'is_subscribed', 'created_at']
        read_only_fields = ['id', 'created_at']


class ContactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['email', 'name', 'company', 'tags']
