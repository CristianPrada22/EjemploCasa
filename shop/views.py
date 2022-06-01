import json
import datetime
from django.http import request, JsonResponse, response, Http404
from django.shortcuts import reverse, get_object_or_404, redirect, render
from django.views import generic
from django.core.mail import send_mail
from django.conf import settings 
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required

from paypalcheckoutsdk.orders import OrdersGetRequest
from shop.paypal import PayPalClient

from shop.forms import Contactf, AddToCartForm, AddressForm
from shop.models import Category, Product, OrderItem, SubCategory, Address, Order, Payment
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

class CheckoutView(LoginRequiredMixin, generic.FormView):
    template_name = 'checkout.html'
    form_class = AddressForm

    def get_success_url(self):
        return reverse("shop:payment")

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        selected_shipping_address = form.cleaned_data.get('selected_shipping_address')
        selected_billing_address = form.cleaned_data.get('selected_billing_address')

        if selected_shipping_address:
            order.shipping_address = selected_shipping_address
        else:
            address = Address.objects.create(
                address_type = 'S',
                user = self.request.user,
                address_line_1=form.cleaned_data['shipping_address_line_1'],
                zip_code=form.cleaned_data['shipping_zip_code'],
                city=form.cleaned_data['shipping_city'],
            )
            order.shipping_address = address

        if selected_billing_address:
            order.billing_address = selected_billing_address
        else:
            address = Address.objects.create(
                address_type = 'B',
                user = self.request.user,
                address_line_1=form.cleaned_data['billing_address_line_1'],
                zip_code=form.cleaned_data['billing_zip_code'],
                city=form.cleaned_data['billing_city'],
            )
            order.billing_address = address

        order.save()
        messages.info(
            self.request, "You have successfully added your addresses")
        return super(CheckoutView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context['order'] = get_or_set_order_session(self.request)
        return context

class PaymentView(generic.TemplateView):
    template_name = 'payment.html'
    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context["PAYPAL_CLIENT_ID"] = "ARZk3IYo3IZ4VLsf6tKoFxLkJzxV6_Ywg8-8SeLq19C67NsvAuTIeDtILVJ0gUgnXoPuEFqOxJSyW5"
        context['order'] = get_or_set_order_session(self.request)
        return context

@login_required
def PaymentComplete(request):
    PPClient = PayPalClient()
    body = json.loads(request.body)
    data = body["orderID"]
    order = get_or_set_order_session(request)
    requestorder = OrdersGetRequest(data)
    response = PPClient.client.execute(requestorder)

    total_paid = response.result.purchase_units[0].amount.value
    payment = Payment.objects.create(
        order=order,
        full_name=response.result.purchase_units[0].shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=response.result.purchase_units[0].shipping.address.address_line_1,
        city=response.result.purchase_units[0].shipping.address.admin_area_2,
        postal_code=response.result.purchase_units[0].shipping.address.postal_code,
        country_code=response.result.purchase_units[0].shipping.address.country_code,
        total_paid=response.result.purchase_units[0].amount.value,
        order_key=response.result.id,
        payment_option="paypal",
        billing_status=True,
    )
    order.ordered = True
    order.ordered_date = datetime.date.today()
    order.save()
    return JsonResponse("Payment completed!", safe=False)

class PaymentCompleteView(generic.TemplateView,LoginRequiredMixin):
    template_name = "payment_successful.html"