from django.db.models.query import InstanceCheckMeta
from django.http import request, JsonResponse, response, Http404
from django.shortcuts import reverse, get_object_or_404, redirect, render
from django.views import generic
from django.core.mail import send_mail
from django.conf import settings 
from django.contrib import messages 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from shop.forms import Contactf, AddToCartForm
from shop.models import Category, Product, OrderItem, SubCategory
from shop.utils import get_or_set_order_session



# Create your views here.


class ContactView(generic.FormView):
    form_class = Contactf
    template_name = "contact.html"

    def get_success_url(self):        
        return reverse("shop:contact")
    
    def form_valid(self, form):
        messages.info(
            self.request, "We have received your message ")
        Name = form.cleaned_data.get('Name')
        Last_name = form.cleaned_data.get('Last_name')
        Email = form.cleaned_data.get('Email')
        Message = form.cleaned_data.get('Message')

        full_message = f"""
            Message received from {Name},{Last_name}, {Email}
            ___________________________________


            {Message}
            """
        send_mail(
            subject="Message received by Contact Form",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL]
        )
        return super(ContactView, self).form_valid(form)

def search(request):
    if request.method == "POST":
        search = request.POST['search']
        product = Product.objects.filter(title__icontains=search)
        return render(request, 'product_list.html', {'search':search, 'product':product})
    else:
        return render(request, 'product_list.html', {})

def ProductListView(request, parent_or_child=None, pk=None):
    categories = Category.objects.filter(parent=None)
    
    if parent_or_child is None:
        products = Product.objects.all()
        paginator = Paginator(products, 6)
            
    elif parent_or_child == 'child':
        sub_cat= SubCategory.objects.get(pk=pk)
        products= sub_cat.product_set.all()
        paginator = Paginator(products, 6)
            
    elif parent_or_child == 'parent':
        products= []
        sub_cats= Category.objects.get(pk=pk).children.all()

        for sub_cat in sub_cats:
            prds = sub_cat.product_set.all()
            products += prds
        paginator = Paginator(products, 6)
            
    else:
        products = []        
          
    page = request.GET.get('page')
 
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products= paginator.page(paginator.num_pages)

    return render(
        request,
        'product_list.html',
        {'categories': categories, 'products': products, }
    )
    
class ProductDetailView(generic.FormView):
    template_name='product_detail.html'
    form_class = AddToCartForm
    
    def get_object(self):
        return get_object_or_404(Product, slug = self.kwargs["slug"])

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            order = get_or_set_order_session(self.request)
            product = self.get_object()
            form = self.form_class(request.POST)
            item_filter = order.items.filter(product = product)

            if form.is_valid():
                if item_filter.exists():
                    item = item_filter.first()
                    item.quantity += int(form.cleaned_data['quantity'])
                    item.save()
                    msg = "sumar item"
                    error = form.errors
                else:
                    new_item = form.save(commit=False)
                    new_item.product = product
                    new_item.order = order
                    new_item.save()
                    msg = "nuevo item"
                    error = form.errors
                response = JsonResponse({'mensaje':msg,'error':error})
                return response    
            else:
                msg = "form no valido"
                error = form.errors
                response = JsonResponse({'mensaje':msg,'error':error})
                print(form.errors)
                return response
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['product'] = self.get_object()
        return context

class CartView(generic.TemplateView):
    template_name = "cart.html"
    def get_context_data(self, *args,**kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context["order"] = get_or_set_order_session(self.request)
        return context

class IncreaseQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.quantity += 1
        order_item.save()
        return redirect("shop:summary")

class DecreaseQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])

        if order_item.quantity <= 1:
            order_item.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        return redirect("shop:summary")

class RemoveFromCartView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.delete()
        return redirect("shop:summary")
