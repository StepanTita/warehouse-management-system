# Generated by Django 2.2.6 on 2020-05-23 11:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cargos_main', '0010_auto_20200519_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='rate',
            field=models.IntegerField(default=0),
        ),
    ]
