from calendar import c
from django.shortcuts import render
from django.views import generic
from shop.models import Product
from article.models import Article

class Shop(generic.ListView):
    template_name = "indexx.html"
    queryset = Product.objects.all()

class Home(generic.ListView):
    template_name = "home.html"
    queryset = Article.objects.all().order_by("-id")
    paginate_by = 6
    def get_context_data(self, **kwargs):
       context = super(Home, self).get_context_data(**kwargs)
       context['publish_list'] = Article.objects.all().order_by("-id")[:5]
       context['product_list'] = Product.objects.all()
       return context
