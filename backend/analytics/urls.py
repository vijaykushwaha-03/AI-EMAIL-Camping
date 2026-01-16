from django.urls import path
from .views import dashboard, campaign_analytics

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('campaign/<uuid:campaign_id>/', campaign_analytics, name='campaign_analytics'),
]
