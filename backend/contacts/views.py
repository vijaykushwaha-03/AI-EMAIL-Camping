from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import csv
import io

from .models import Contact
from .serializers import ContactSerializer, ContactCreateSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ContactCreateSerializer
        return ContactSerializer
    
    def get_queryset(self):
        queryset = Contact.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                email__icontains=search
            ) | queryset.filter(
                name__icontains=search
            )
        return queryset
    
    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def import_csv(self, request):
        """Import contacts from CSV file"""
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not file.name.endswith('.csv'):
            return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)
        
        decoded = file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(decoded))
        
        imported = 0
        skipped = 0
        
        for row in reader:
            email = None
            name = ''
            company = ''
            
            for key, value in row.items():
                key_lower = key.lower().strip()
                if key_lower in ['email', 'email address', 'mail']:
                    email = value.strip()
                elif key_lower in ['name', 'full name', 'fullname']:
                    name = value.strip()
                elif key_lower in ['company', 'company name', 'organization']:
                    company = value.strip()
            
            if not email:
                skipped += 1
                continue
            
            if Contact.objects.filter(email=email).exists():
                skipped += 1
                continue
            
            Contact.objects.create(email=email, name=name, company=company)
            imported += 1
        
        return Response({
            'message': 'Import complete',
            'imported': imported,
            'skipped': skipped
        })
