# Generated by Django 2.2.9 on 2021-04-03 20:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0008_auto_20210403_2355'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Folllows',
            new_name='Follow',
        ),
    ]
