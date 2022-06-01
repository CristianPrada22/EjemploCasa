"""project_name URL Configuration

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
from argparse import Namespace
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from main import views 
from Menus.views import sitemap
from pages.views import view_page

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', views.Home.as_view(),name="Home"),
    path(_('admin/doc/'), include('django.contrib.admindocs.urls')),
    path(_('admin/'), admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('main/', include('main.urls', namespace='main')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('hr/', include('hr.urls', namespace='hr')),
    path('article/', include('article.urls', namespace='article')), 
    re_path(r'^sitemap/$', sitemap),
    re_path( r'^public/admin/pages/', include('pages.urls') ),
    re_path(r'^(?P<url>.*)$', view_page),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)