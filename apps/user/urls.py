from rest_framework import routers

from apps.user import views

router = routers.DefaultRouter()
router.register('v1/users', views.UserAPIView, basename='user')
urlpatterns = router.urls
