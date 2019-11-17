# Generated by Django 2.2.5 on 2019-11-09 23:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cargos_main', '0004_storage_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateNotifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed', models.BooleanField(default=False)),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cargos_main.Cargo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
