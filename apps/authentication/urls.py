from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.authentication.versions.v1.views import auth_view

router = routers.DefaultRouter()
router.register('v1/auth', auth_view.JWTAuthAPIView, basename='auth')

urlpatterns = [
    url('', include(router.urls)),
]
