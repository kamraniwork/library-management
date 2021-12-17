from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom User Manager for User Model in users/models.py
    """

    def create_user(self, username=None, email=None, phone=None, password=None, **extra_fields):
        user = self.model(username=username, phone=phone, email=self.normalize_email(email),
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user


def create_superuser(self, username, phone, email, password, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault('is_active', True)
    extra_fields.setdefault('first_name', 'admin')

    if extra_fields.get('is_staff') is not True:
        raise ValueError('Superuser must have is_staff = True.')

    if extra_fields.get('is_superuser') is not True:
        raise ValueError('Superuser must have is_superuser = True.')

    return self.create_user(username=username, phone=phone, email=email, password=password,
                            **extra_fields)
