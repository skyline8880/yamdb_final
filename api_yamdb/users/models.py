from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
]


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='email')
    role = models.CharField(
        max_length=25, verbose_name='role', choices=ROLES, default=ROLES[0][0]
    )
    bio = models.TextField(
        max_length=500, blank=True, verbose_name='biography'
    )
    confirmation_code = models.CharField(
        max_length=60, blank=True, verbose_name='confirmation code'
    )

    @property
    def is_admin(self):
        return self.role == ROLES[-1][0] or self.is_staff

    @property
    def is_moderator(self):
        return self.role == ROLES[1][0]
