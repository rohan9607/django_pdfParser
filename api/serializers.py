from rest_framework import serializers
from api.models import Company

# Serializer to transform model into json format
class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Company
        fields="__all__"
        
    