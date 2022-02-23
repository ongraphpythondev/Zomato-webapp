# Generated by Django 3.2.8 on 2021-11-11 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_delete_res_name'),
        ('customer', '0014_menuitem_restaurant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='restaurant',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='restaurant',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant_model'),
        ),
    ]