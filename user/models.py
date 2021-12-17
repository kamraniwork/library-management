from django.db import models
from .managers import UserManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for better management authenticated
    """
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile'
    )

    activation_date = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
