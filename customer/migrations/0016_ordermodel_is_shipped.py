# Generated by Django 3.2.9 on 2021-11-15 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0015_auto_20211111_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='is_shipped',
            field=models.BooleanField(default=False),
        ),
    ]
