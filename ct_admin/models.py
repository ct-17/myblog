from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class PinnedApplication(models.Model):
    app_label = models.CharField(verbose_name=_('application name'), max_length=255)
    user = models.PositiveIntegerField(verbose_name=_('user'))
    date_add = models.DateTimeField(verbose_name=_('date created'), default=timezone.now)

    class Meta:
        verbose_name = _('pinned application')
        verbose_name_plural = _('pinned applications')
        ordering = ('date_add',)

    def __str__(self):
        return self.app_label