from django.conf.urls import url
from django.urls import include
from apps.health_check.views import ping

urlpatterns = [
    url('', include('apps.authentication.urls')),
    url('ping', ping),
]
