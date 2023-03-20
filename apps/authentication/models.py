from django.db import models
from apps.core.models import UuidModel
from django.conf import settings


class UserActivity(UuidModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=63)
    created_at = models.DateTimeField(auto_now_add=True)
