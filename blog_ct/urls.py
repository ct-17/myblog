"""blog_ct URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from accounts.views import RegisterView, LoginView
import django.contrib.auth as auth_view
from django.contrib.auth.views import LogoutView
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include(('blog.urls', 'blog'), namespace='blog')),
    path('search/', include(('search.urls', 'search'), namespace='search')),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    prefix_default_language=True,
)



if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)