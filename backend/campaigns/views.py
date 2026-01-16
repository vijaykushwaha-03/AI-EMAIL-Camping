from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .models import Campaign, EmailLog
from .serializers import CampaignSerializer, CampaignCreateSerializer


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CampaignCreateSerializer
        return CampaignSerializer
    
    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """Send campaign to all recipients"""
        campaign = self.get_object()
        
        if campaign.status == 'sent':
            return Response(
                {'error': 'Campaign already sent'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        test_mode = request.data.get('test_mode', False)
        
        # Get recipients
        contacts = campaign.recipients.filter(is_subscribed=True)
        if not contacts.exists():
            # If no specific recipients, send to all subscribed
            from contacts.models import Contact
            contacts = Contact.objects.filter(is_subscribed=True)
        
        if not contacts.exists():
            return Response(
                {'error': 'No recipients found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Limit to 1 in test mode
        if test_mode:
            contacts = contacts[:1]
        
        campaign.status = 'sending'
        campaign.save()
        
        sent = 0
        failed = 0
        
        # Send emails
        for contact in contacts:
            try:
                self._send_email(
                    to_email=contact.email,
                    subject=campaign.subject,
                    html_body=campaign.content,
                    cc_email=campaign.cc_email,
                    bcc_email=campaign.bcc_email
                )
                EmailLog.objects.create(
                    campaign=campaign,
                    contact=contact,
                    status='sent'
                )
                sent += 1
            except Exception as e:
                print(f"Error sending to {contact.email}: {e}")
                EmailLog.objects.create(
                    campaign=campaign,
                    contact=contact,
                    status='failed'
                )
                failed += 1
        
        campaign.sent_count = sent
        campaign.status = 'sent'
        campaign.save()
        
        return Response({
            'campaign_id': str(campaign.id),
            'sent': sent,
            'failed': failed,
            'message': f'Campaign sent to {sent} recipients'
        })
    
    def _send_email(self, to_email, subject, html_body, cc_email=None, bcc_email=None):
        """Send a single email via SMTP"""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL_ADDRESS
        msg['To'] = to_email
        
        recipients = [to_email]
        
        if cc_email:
            msg['Cc'] = cc_email
            recipients.append(cc_email)
            
        if bcc_email:
            # BCC is not added to headers, but added to recipients list
            recipients.append(bcc_email)
        
        msg.attach(MIMEText(html_body, 'html'))
        
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        server.sendmail(settings.EMAIL_ADDRESS, recipients, msg.as_string())
        server.quit()
