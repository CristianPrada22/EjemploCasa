# general imports
from django import views
from django.urls import path
from main import views

app_name = 'main'
urlpatterns = [
    path('', views.Home.as_view(),name="Home"),
    path('shop/', views.Shop.as_view(), name="shop")    
]
