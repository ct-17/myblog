# Generated by Django 2.2.7 on 2019-12-11 14:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_postmodel_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postmodel',
            name='like',
        ),
        migrations.AddField(
            model_name='postmodel',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]