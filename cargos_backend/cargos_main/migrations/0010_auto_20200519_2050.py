# Generated by Django 2.2.6 on 2020-05-19 20:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('cargos_main', '0009_auto_20200519_2041'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='categorization',
            unique_together={('category', 'company')},
        ),
    ]