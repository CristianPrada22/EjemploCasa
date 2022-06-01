# general imports
from django import views
from django.urls import path
from main import views
#from main.views import Home

 #api imports

 #api urls

 #general urls
app_name = 'main'
urlpatterns = [
    #path('', views.Home.as_view, name="home"),
    #path('', home, name="home"),
    path('', views.Home.as_view(),name="Home"),    
]
