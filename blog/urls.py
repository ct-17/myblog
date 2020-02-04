from django.urls import path, re_path
from django.conf.urls import url, include
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
    PostLike,
    PostLikeAPI,
    )

urlpatterns = [
    path('', Home, name='home'),
    path('windows/', windows, name='windows'),
    path('linux/', linux, name='linux'),
    path('technology/', technology, name='technology'),
    path('entertain/', entertain, name='entertain'),
    path('create/', post_model_create_view, name='create'),
    path('<str:kind>/<slug:slug>/', BlogDetailSlugView.as_view(), name='detail'),
    path('<str:kind>/<slug:slug>/like/', PostLike.as_view(), name='like'),
    path('<str:kind>/<slug:slug>/like-api/', PostLikeAPI.as_view(), name='like-api'),
    re_path(r'^(?P<id>\d+)/delete/$', post_model_delete_view, name='delete'),
    re_path(r'^(?P<id>\d+)/edit/$', post_model_update_view, name='update'),
]