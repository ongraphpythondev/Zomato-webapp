# Generated by Django 3.2.8 on 2021-11-10 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_remove_menuitem_restaurant_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='menuitem',
            name='restaurant_id',
            field=models.ManyToManyField(related_name='item', to='customer.Menu_list'),
        ),
    ]