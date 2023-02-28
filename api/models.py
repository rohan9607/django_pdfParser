from django.db import models

# Create your models here.

# Company Models
class Company(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    location=models.CharField(max_length=50)
    about=models.CharField(max_length=50)
    type=models.CharField(max_length=100, choices=
                          (("IT", "IT"), ("NON-IT", "NON-IT"), ("Mobile", "Mobile")))
    created_date=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=True)
    
#Employee Model