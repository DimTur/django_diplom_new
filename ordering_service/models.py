from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from rest_framework.exceptions import ValidationError

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
    type = models.CharField(
        verbose_name='Тип пользователя',
        choices=USER_TYPE_CHOICES, max_length=5,
        default='buyer'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['type', 'last_name', 'first_name', 'patronymic', 'company', 'position']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Address(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        related_name='contacts',
        blank=True,
        on_delete=models.CASCADE
    )
    city = models.CharField(
        max_length=20,
        verbose_name='Город'
    )
    street = models.CharField(
        max_length=80,
        verbose_name='Улица'
    )
    house = models.CharField(
        max_length=10,
        verbose_name='Дом'
    )
    structure = models.CharField(
        max_length=10,
        verbose_name='Корпус',
        blank=True
    )
    building = models.CharField(
        max_length=10,
        verbose_name='Строение',
        blank=True
    )
    apartment = models.CharField(
        max_length=10,
        verbose_name='Квартира',
        blank=True
    )

    def __str__(self):
        return f'{self.city}, {self.street}, {self.house}'

    def clean(self):
        # Получаем количество адресов, связанных с пользователем
        existing_addresses = Address.objects.filter(user=self.user)
        num_existing_addresses = existing_addresses.count()

        # если пользователь имеет уже 5 адресов, выдаем ошибку
        if num_existing_addresses >= 5:
            raise ValidationError(f"{self.user} у пользователя максимальное количество адресов")

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Список адресов'
        unique_together = ('user',)


class Contact(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        related_name='contacts',
        blank=True,
        on_delete=models.CASCADE
    )
    phone = models.CharField(
        max_length=12,
        verbose_name='Телефон'
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Информаци о контакте {self.user}'

    def clean(self):
        existing_addresses = Address.objects.filter(user=self.user)
        num_existing_addresses = existing_addresses.count()
        if num_existing_addresses >= 5:
            raise ValidationError(f"{self.user} у пользователя максимальное количество адресов")
        #
        # # Check that the address belongs to the user
        # if self.address and self.address.user != self.user:
        #     raise ValidationError("The selected address does not belong to the user")

    class Meta:
        verbose_name = 'Контакты'
        unique_together = ('user',)
