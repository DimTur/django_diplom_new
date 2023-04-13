from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from ordering_service.managers import CustomUserManager

USER_TYPE_CHOICES = (
    ('shop', 'Магазин'),
    ('buyer', 'Покупатель'),
)

STATE_CHOICES = (
    ('basket', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
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
    type = models.CharField(verbose_name='Тип пользователя', choices=USER_TYPE_CHOICES, max_length=5, default='buyer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['type', 'last_name', 'first_name', 'patronymic', 'company', 'position']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Address(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', related_name='addressies',
                             on_delete=models.CASCADE)
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
        verbose_name_plural = 'Адреса'


class Contact(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', related_name='contacts',
                             on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL,
                                null=True, blank=True)

    def __str__(self):
        return f'Информаци о контакте {self.user}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        unique_together = ('user',)


class Shop(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', related_name='shops', blank=True,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Название магазина', unique=True)
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True)
    filename = models.TextField(max_length=100, verbose_name='Имя файла', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ('-name',)


class Category(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', related_name='categories',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Название категории', unique=True)
    shops = models.ManyToManyField(Shop, verbose_name='Магазины', related_name='categories', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-name',)


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя товара')
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='products', on_delete=models.CASCADE,
                                 blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('-name',)


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, verbose_name='Имя товара', related_name='products_info',
                                on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='products_info', on_delete=models.CASCADE)
    model = models.CharField(max_length=100, verbose_name='Модель')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена')

    class Meta:
        verbose_name = 'Информация о товаре'
        verbose_name_plural = 'Информация о товарах'
        constraints = [
            models.UniqueConstraint(fields=['product', 'shop'], name='unique_product_info'),
        ]


class Parameter(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название параметра')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Название параметра'
        verbose_name_plural = 'Параметры'
        ordering = ('-name',)


class ProductInfoParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, verbose_name='Информация о товаре',
                                     related_name='product_info_parameters', on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, verbose_name='Название параметра',
                                  related_name='product_info_parameters', on_delete=models.CASCADE, blank=True)
    value = models.CharField(max_length=100, verbose_name='Значение')

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Список параметров'
        constraints = [
            models.UniqueConstraint(fields=['product_info', 'parameter'], name='unique_product_parameter'),
        ]


class Order(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', related_name='orderies',
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(verbose_name='Статус', choices=STATE_CHOICES, max_length=15)
    contact = models.ForeignKey(Contact, verbose_name='Контакты покупателя',
                                on_delete=models.CASCADE, blank=True, null=True)
    address = models.ForeignKey(Address, verbose_name='Адрес', on_delete=models.CASCADE,
                                blank=True, null=True)

    def __str__(self):
        return self.created_at

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created_at',)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='order_products', on_delete=models.CASCADE,
                              blank=True)
    product_info = models.ForeignKey(ProductInfo, verbose_name='Заказываемый товар', related_name='order_products',
                                     on_delete=models.CASCADE, blank=True)
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'
        constraints = [
            models.UniqueConstraint(fields=['order', 'product_info'], name='unique_order_product'),
        ]
