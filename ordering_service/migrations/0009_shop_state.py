# Generated by Django 4.2 on 2023-04-27 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering_service', '0008_alter_productinfoparameter_product_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='state',
            field=models.BooleanField(default=True, verbose_name='Открыт для получения заказов'),
        ),
    ]