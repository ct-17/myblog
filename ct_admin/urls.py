from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import Home

urlpatterns = [
    url(r'^$', Home, name='home')
]