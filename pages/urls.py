from unicodedata import name
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from pages.api.views import PageAPIView

router = routers.DefaultRouter()
router.register(r'pages', PageAPIView, 'page')

urlpatterns = [
    path('^api/', include(router.urls)),    
]