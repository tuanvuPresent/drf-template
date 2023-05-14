from apps.core.repository import RepositoryBase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRepository(RepositoryBase):
    class Meta:
        model = User
