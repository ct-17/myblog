import re
from datetime import timedelta, datetime, date
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.utils.encoding import smart_text
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField

PUBLISH_CHOICES = [
        ('windows', _('windows')),
        ('linux', _('linux')),
        ('technology', _('technology')),
        ('entertainment', _('entertainment')),
    ]

def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s

class PostModelQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def kind(self):
        return self.filter(kind="windows")

    def post_title_items(self, value):
        return self.filter(title__icontains=value)

    def search(self, query):
        lookups = (Q(title__icontains=query) | 
                  Q(content__icontains=query)
                  )
        return self.filter(lookups).distinct()


class PostModelManager(models.Manager):
    def get_queryset(self):
        return PostModelQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        qs = self.get_queryset().active()
        return qs

    def get_timeframe(self, date1, date2):
        #giả định đối tượng datetime
        qs = self.get_queryset()
        qs_time_1 = qs.filter(publish_date__gte=date1)
        qs_time_2 = qs_time_1.filter(publish_date__lt=date2) # Q Lookups
        return qs_time_2

    def search(self, query):
        return self.get_queryset().active().search(query)

class PostModel(models.Model):
    id              = models.BigAutoField(primary_key=True)
    active          = models.BooleanField(default=True) # trống trong cơ sở dữ liệu
    title           = models.CharField(
                            max_length=240, 
                            verbose_name=_('Title:'), 
                            unique=True,
                            error_messages={
                                "unique": _("This title is not unique, please try again."),
                                "blank": _("This field is required, please try again.")
                            },
                            help_text=_('The title must be unique.'))
    slug            = models.SlugField(null=True, blank=True, )
    description     = models.CharField(null=True, blank=True, verbose_name=_('Description:'), max_length=1000)
    content         = RichTextUploadingField(null=True, blank=True, verbose_name=_('Content:'))
    kind            = models.CharField(max_length=120, choices=PUBLISH_CHOICES, verbose_name=_('Kind:'))
    view_count      = models.IntegerField(default=0, verbose_name=_('Views:'))
    publish_date    = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now, verbose_name=_('Publish Date:'))
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, verbose_name=_('Author:'), related_name='author_blog1')
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    like            = models.IntegerField(default=0, verbose_name=_("Like:"))

    objects = PostModelManager()
    other = PostModelManager()

    def save(self, *args, **kwargs):
        slug_title = no_accent_vietnamese(self.title)
        self.slug = slugify(slug_title)
        self.description = self.title
        self.kind = 'entertainment'
        super(PostModel, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Post')

    def __unicode__(self): #python 2
        return smart_text(self.title) #self.title

    def __str__(self): #python 3
        return smart_text(self.title)

def blog_post_model_pre_save_receiver(sender, instance, *args, **kwargs):
    # print("trước khi lưu")
    if not instance.slug and instance.title:
        instance.slug = slugify(instance.title) 

pre_save.connect(blog_post_model_pre_save_receiver, sender=PostModel)

def blog_post_model_post_save_receiver(sender, instance, created, *args, **kwargs):
    # print("sau khi lưu")
    # print(created)
    if created:
        if not instance.slug and instance.title:
            instance.slug = slugify(instance.title)
            instance.save()

post_save.connect(blog_post_model_post_save_receiver, sender=PostModel)


class Comment(models.Model):
    post = models.ForeignKey(PostModel, on_delete= models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='author_blog2')
    body = models.TextField(verbose_name=_("Comment"))
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comment')