# Generated by Django 4.2 on 2023-05-03 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering_service', '0010_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Количество'),
        ),
    ]
