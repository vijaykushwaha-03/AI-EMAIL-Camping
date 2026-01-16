from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

from campaigns.models import Campaign, EmailLog
from contacts.models import Contact


@api_view(['GET'])
def dashboard(request):
    """Get dashboard statistics"""
    
    # Total stats
    total_contacts = Contact.objects.count()
    total_sent = EmailLog.objects.exclude(status='failed').count()
    total_opened = EmailLog.objects.filter(opened_at__isnull=False).count()
    total_clicked = EmailLog.objects.filter(clicked_at__isnull=False).count()
    total_bounced = EmailLog.objects.filter(status='bounced').count()
    
    # Calculate rates
    open_rate = round(total_opened / total_sent * 100, 1) if total_sent > 0 else 0
    click_rate = round(total_clicked / total_sent * 100, 1) if total_sent > 0 else 0
    bounce_rate = round(total_bounced / total_sent * 100, 1) if total_sent > 0 else 0
    
    # Chart data - last 7 days
    chart_data = []
    for i in range(6, -1, -1):
        date = timezone.now().date() - timedelta(days=i)
        date_start = timezone.datetime.combine(date, timezone.datetime.min.time())
        date_end = timezone.datetime.combine(date, timezone.datetime.max.time())
        
        if timezone.is_aware(timezone.now()):
            date_start = timezone.make_aware(date_start)
            date_end = timezone.make_aware(date_end)
        
        sent_count = EmailLog.objects.filter(
            sent_at__gte=date_start,
            sent_at__lte=date_end
        ).count()
        
        opened_count = EmailLog.objects.filter(
            opened_at__gte=date_start,
            opened_at__lte=date_end
        ).count()
        
        chart_data.append({
            'date': date.strftime("%b %d"),
            'sent': sent_count,
            'opened': opened_count
        })
    
    # Recent campaigns
    recent_campaigns = []
    for c in Campaign.objects.all()[:5]:
        recent_campaigns.append({
            'id': str(c.id),
            'name': c.name,
            'status': c.status,
            'open_rate': c.open_rate,
            'created_at': c.created_at.isoformat()
        })
    
    return Response({
        'stats': {
            'total_sent': total_sent,
            'total_contacts': total_contacts,
            'open_rate': open_rate,
            'click_rate': click_rate,
            'bounce_rate': bounce_rate
        },
        'chart_data': chart_data,
        'recent_campaigns': recent_campaigns
    })


@api_view(['GET'])
def campaign_analytics(request, campaign_id):
    """Get detailed analytics for a campaign"""
    try:
        campaign = Campaign.objects.get(id=campaign_id)
    except Campaign.DoesNotExist:
        return Response({'error': 'Campaign not found'}, status=404)
    
    logs = EmailLog.objects.filter(campaign=campaign)
    
    return Response({
        'campaign_id': str(campaign.id),
        'name': campaign.name,
        'sent_count': campaign.sent_count,
        'open_count': campaign.open_count,
        'click_count': campaign.click_count,
        'open_rate': campaign.open_rate,
        'click_rate': campaign.click_rate,
        'logs': [
            {
                'email': log.contact.email,
                'status': log.status,
                'sent_at': log.sent_at.isoformat() if log.sent_at else None,
                'opened_at': log.opened_at.isoformat() if log.opened_at else None
            }
            for log in logs[:50]
        ]
    })
