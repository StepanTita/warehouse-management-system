# Generated by Django 2.2.6 on 2020-05-23 10:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0006_auto_20200523_1019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='social_links',
        ),
        migrations.DeleteModel(
            name='SocialNetworks',
        ),
    ]
