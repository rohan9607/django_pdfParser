from django.urls import path
from . import views
urlpatterns = [
    path("fileparse/", views.parseFile)
]
