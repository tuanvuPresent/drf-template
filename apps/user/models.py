from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.user.constant import UserType, UserGender


class User(AbstractUser):
    username = models.CharField(max_length=63, unique=True)
    email = models.EmailField(max_length=63, unique=True, null=True)
    user_type = models.IntegerField([(item.value, item.value) for item in UserType],
                                    default=UserType.STAFF.value)
    is_staff = models.BooleanField(default=False)
    gender = models.IntegerField(choices=[(item.value, item.value) for item in UserGender],
                                 default=UserGender.MALE.value)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_verify_email = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'authentication_user'


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'authentication_token'

    def __str__(self):
        return f"{self.id} - {self.user_id} - {self.token}"
