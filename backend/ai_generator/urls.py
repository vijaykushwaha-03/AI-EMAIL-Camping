from django.urls import path
from .views import generate_email

urlpatterns = [
    path('generate/', generate_email, name='generate_email'),
]
