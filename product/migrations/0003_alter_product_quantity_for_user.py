# Generated by Django 5.1.3 on 2024-11-16 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_quantity_for_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity_for_user',
            field=models.IntegerField(default=1),
        ),
    ]