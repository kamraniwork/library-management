from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom User Manager for User Model in users/models.py
    """

    def create_user(self, username=None, email=None, phone=None, password=None, **extra_fields):
        if email is None or phone is None:
            user = self.model(username=username, **extra_fields)
        else:
            user = self.model(username=username, email=email, phone=phone ** extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('first_name', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True.')

        return self.create_user(username=username, password=password,
                                **extra_fields)
