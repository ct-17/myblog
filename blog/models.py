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
from froala_editor.fields import FroalaField
from django.urls import reverse
from accounts.models import User

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
    active          = models.BooleanField(default=True, editable=False)
    title           = models.CharField(
                            max_length=240, 
                            verbose_name=_('Title:'), 
                            unique=True,
                            error_messages={
                                "unique": _("This title is not unique, please try again."),
                                "blank": _("This field is required, please try again.")
                            },
                            help_text=_('The title must be unique.'))
    slug            = models.SlugField(null=True, blank=True, max_length=300)
    description     = models.CharField(null=True, blank=True, verbose_name=_('Description:'), max_length=1000)
    img             = models.ImageField(null=True, blank=True, upload_to='uploads/images/%Y/%m/%d/', verbose_name=_('Image:'))
    content         = FroalaField(null=True, blank=True, verbose_name=_('Content:'))
    # content         = models.TextField(null=True, blank=True, verbose_name=_('Content:'))
    kind            = models.CharField(max_length=120, choices=PUBLISH_CHOICES, verbose_name=_('Kind:'), default='entertainment')
    view_count      = models.IntegerField(default=0, verbose_name=_('Views:'), editable=False)
    publish_date    = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now, verbose_name=_('Publish Date:'), editable=False)
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, verbose_name=_('Author:'), related_name='author_blog1')
    updated         = models.DateTimeField(auto_now=True, editable=False)
    timestamp       = models.DateTimeField(auto_now_add=True, editable=False)
    like            = models.ManyToManyField(User, blank=True, related_name='post_likes')

    objects = PostModelManager()
    other = PostModelManager()

    def save(self, *args, **kwargs):
        slug_title = no_accent_vietnamese(self.title)
        self.slug = slugify(slug_title)
        self.description = self.title
        super(PostModel, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Post')

    def __str__(self): #python 3
        return smart_text(self.title)
    
    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"kind": self.kind, "slug": self.slug})

    def get_like_url(self):
        return reverse("blog:like", kwargs={"kind": self.kind, "slug": self.slug})

    def get_api_like_url(self):
        return reverse("blog:like-api", kwargs={"kind": self.kind, "slug": self.slug})

def blog_post_model_pre_save_receiver(sender, instance, *args, **kwargs):
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

class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs
    
    def reply(self):
        qs = super(CommentManager, self).filter(parent=self.instance)
        return qs

    def filter_by_instance(self, instance):
        obj_id = instance.id
        qs = super(CommentManager, self).filter(post= obj_id).filter(parent=None)
        return qs

class Comment(models.Model):
    post = models.ForeignKey(PostModel, on_delete= models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, verbose_name=_('Author:'), related_name='author_blog2')
    body = models.TextField(verbose_name=_("Comment"))
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete= models.CASCADE, related_name='replys')

    objects = CommentManager()

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comment')
        ordering = ['-date']

    def replys(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
