# Generated by Django 5.1.3 on 2024-11-24 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='order_status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]