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
                            choices=USER_TYPE_CHOICES, max_length=5, default='buyer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['type', 'last_name', 'first_name', 'patronymic', 'company', 'position']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Address(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь',
                             related_name='addressies', blank=True, on_delete=models.CASCADE)
    city = models.CharField(max_length=20, verbose_name='Город')
    street = models.CharField(max_length=80, verbose_name='Улица')
    house = models.CharField(max_length=10, verbose_name='Дом')
    structure = models.CharField(max_length=10, verbose_name='Корпус', blank=True)
    building = models.CharField(max_length=10, verbose_name='Строение', blank=True)
    apartment = models.CharField(max_length=10, verbose_name='Квартира', blank=True)

    def __str__(self):
        return f'{self.city}, {self.street}, {self.house}'

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Список адресов'


class Contact(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь',
                             related_name='contacts', blank=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Информаци о контакте {self.user}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Список контактов'
        unique_together = ('user',)
