# Generated by Django 4.1.7 on 2023-04-03 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ordering_service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=20, verbose_name='Город')),
                ('street', models.CharField(max_length=80, verbose_name='Улица')),
                ('house', models.CharField(max_length=10, verbose_name='Дом')),
                ('structure', models.CharField(blank=True, max_length=10, verbose_name='Корпус')),
                ('building', models.CharField(blank=True, max_length=10, verbose_name='Строение')),
                ('apartment', models.CharField(blank=True, max_length=10, verbose_name='Квартира')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='addressies', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Адрес',
                'verbose_name_plural': 'Список адресов',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=12, verbose_name='Телефон')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ordering_service.address')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Контакты',
                'unique_together': {('user',)},
            },
        ),
    ]
