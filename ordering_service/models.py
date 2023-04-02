from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from ordering_service.managers import CustomUserManager

USER_TYPE_CHOICES = (
    ('shop', 'Магазин'),
    ('buyer', 'Покупатель'),
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_name = models.CharField(max_length=30, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    patronymic = models.CharField(max_length=30, blank=True)
    company = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    type = models.CharField(verbose_name='Тип пользователя',
                            choices=USER_TYPE_CHOICES,
                            max_length=5,
                            default='buyer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['type', 'last_name', 'first_name', 'patronymic', 'company', 'position']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
