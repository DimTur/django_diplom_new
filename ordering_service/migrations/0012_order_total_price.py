# Generated by Django 4.2 on 2023-05-06 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering_service', '0011_alter_orderproduct_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
