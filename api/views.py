from django.shortcuts import render
from rest_framework import viewsets
from api.models import Company
from api.serializers import CompanySerializer
# Create your views here.


#Company View
class CompanyView(viewsets.ModelViewSet):
    # Specify the company Model
    queryset=Company.objects.all()
    # Specify the company Serializer
    serializer_class=CompanySerializer
    
    