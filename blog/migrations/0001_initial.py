# Generated by Django 2.2.4 on 2019-08-08 15:50

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PostModel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(error_messages={'blank': 'This field is required, please try again.', 'unique': 'This title is not unique, please try again.'}, help_text='The title must be unique.', max_length=240, unique=True, verbose_name='Title:')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Description:')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Content:')),
                ('kind', models.CharField(choices=[('windows', 'windows'), ('linux', 'linux'), ('technology', 'technology'), ('entertainment', 'entertainment')], max_length=120, verbose_name='Kind:')),
                ('view_count', models.IntegerField(default=0, verbose_name='Views:')),
                ('publish_date', models.DateField(default=django.utils.timezone.now, verbose_name='Publish Date:')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('like', models.IntegerField(default=0, verbose_name='Like:')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_blog1', to=settings.AUTH_USER_MODEL, verbose_name='Author:')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Post',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='Comment')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_blog2', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.PostModel')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comment',
            },
        ),
    ]
