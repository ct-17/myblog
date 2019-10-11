from django.urls import path, re_path
from django.utils.translation import gettext_lazy as _

from .views import (
    post_model_create_view,
    BlogDetailSlugView,
    post_model_delete_view,
    post_model_list_view,
    post_model_update_view,
    Home,
    windows,
    linux,
    technology,
    entertain,
    )

urlpatterns = [
    path('', Home, name='home'),
    path('windows/', windows, name='windows'),
    path('linux/', linux, name='linux'),
    path('technology/', technology, name='technology'),
    path('entertain/', entertain, name='entertain'),
    path('create/', post_model_create_view, name='create'),
    path('<str:kind>/<slug:slug>/', BlogDetailSlugView.as_view(), name='detail'),
    re_path(r'^(?P<id>\d+)/delete/$', post_model_delete_view, name='delete'),
    re_path(r'^(?P<id>\d+)/edit/$', post_model_update_view, name='update'),
]