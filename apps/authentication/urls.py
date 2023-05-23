from django.conf.urls import url
from rest_framework import routers

from apps.authentication.v1 import views

router = routers.DefaultRouter()
router.register('v1/auth', views.JWTAuthAPIView, basename='auth')
urlpatterns = router.urls
