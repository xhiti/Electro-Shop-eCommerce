# Generated by Django 3.2.5 on 2021-07-31 08:15

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_variation'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='variation',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
