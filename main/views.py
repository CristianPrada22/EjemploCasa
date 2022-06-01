#from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from shop.models import Product



class Home(generic.ListView):
    template_name = "indexx.html"
    queryset = Product.objects.all()