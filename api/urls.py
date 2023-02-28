from django.urls import path, include
from rest_framework import routers
from api.views import CompanyView
router = routers.DefaultRouter()
router.register(r"companies", CompanyView)


urlpatterns = [
    path("", include(router.urls))
]
