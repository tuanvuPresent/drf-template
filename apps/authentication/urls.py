from rest_framework import routers

from apps.authentication import views

router = routers.DefaultRouter()
router.register('auth', views.JWTAuthAPIView, basename='auth')
urlpatterns = router.urls
