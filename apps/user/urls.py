from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.user.versions.v1.views import user_view

router = routers.DefaultRouter()
router.register('v1/users', user_view.UserAPIView, basename='user')

urlpatterns = [
    url('', include(router.urls)),
]
