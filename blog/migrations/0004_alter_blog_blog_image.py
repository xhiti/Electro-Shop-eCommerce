# Generated by Django 3.2.5 on 2022-01-03 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_blog_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_image',
            field=models.ImageField(blank=True, default='', upload_to='photos/blog/'),
        ),
    ]
