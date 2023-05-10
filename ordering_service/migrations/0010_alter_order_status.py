# Generated by Django 4.2 on 2023-04-30 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering_service', '0009_shop_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('basket', 'Статус корзины'), ('new', 'Новый'), ('confirmed', 'Подтвержден'), ('assembled', 'Собран'), ('sent', 'Отправлен'), ('delivered', 'Доставлен'), ('canceled', 'Отменен')], default='basket', max_length=15, verbose_name='Статус'),
        ),
    ]