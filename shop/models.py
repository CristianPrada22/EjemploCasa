from tabnanny import verbose
from weakref import proxy
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import DecimalField
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

User = get_user_model()
"""""
Definition of ecommerce models
"""
class Address(models.Model):

    ADDRESS_CHOICES = (
        ('B', _('Billing')),
        ('S', _('Shipping')),
    )

    user = models.ForeignKey(User, verbose_name = _('User'), on_delete=models.CASCADE)
    address_line_1 = models.CharField(
        verbose_name = _('Address line 1'), 
        max_length=150, 
        help_text=_("Register an address "))
    city = models.CharField(
        verbose_name = _('City'), 
        max_length=100, 
        help_text=_("City where the purchase is made"))
    zip_code = models.CharField(
        verbose_name = _('Zip code'), 
        max_length=100, 
        help_text=_("City zip code"))
    address_type = models.CharField(
        verbose_name = _('Address type'), 
        max_length=1, 
        choices=ADDRESS_CHOICES, 
        help_text=_("Allows you to choose between different types of addresses"))
    default = models.BooleanField(
        verbose_name = _('Default'), 
        default=False, 
        help_text=_("Allows to set default address"))
    
    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.zip_code} "

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

class Node(models.Model):
    name = models.CharField(
        verbose_name = _('Name'), 
        max_length=150, 
        help_text=_("Name of category or subcategory")
    )
    parent = models.ForeignKey(
        'self',
        verbose_name=_('Parent'),
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True
    )
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name',]
        verbose_name = _('Node')
        verbose_name_plural = _('Nodes')

class Category(Node):

    class Meta:
        proxy = True
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

class SubCategory(Node):

    class Meta:
        proxy = True
        verbose_name = _('Sub Category')
        verbose_name_plural = _('Sub Categories')

class Product(TranslatableModel):
    """
    class to store a product.
    """
    translations = TranslatedFields(
        title = models.CharField(
        verbose_name = _('Title'), 
        max_length=150, 
        help_text=_("Name of product, example product 1")),

        descritption = models.TextField(
        verbose_name = _('Description'), 
        help_text=_("Here you must write the product description"))
    )
    subcategory = models.ForeignKey(
        SubCategory,
        verbose_name= _('Sub category'),
        on_delete= models.CASCADE
    )
    slug = models.SlugField(
        verbose_name = _('Slug'), 
        unique=True, 
        help_text=_("A short name, generally used in URLs."))
    image = models.ImageField(
        verbose_name = _('Image'), 
        upload_to='product_images')    
    price = models.DecimalField(
        verbose_name = _('Price'), 
        default = 0,
        decimal_places = 2,
        max_digits = 11,
        help_text=_("Price of product"))
    stock = models.IntegerField(
        verbose_name = _('Stock'), 
        default=0, 
        help_text=_("Stock of product"))
    created = models.DateTimeField(
        verbose_name = _('Created'), 
        auto_now_add=True)
    updated = models.DateTimeField(
        verbose_name = _('Updated'), 
        auto_now=True)
    active = models.BooleanField(
        verbose_name = _('Active'), 
        default=False, 
        help_text=_("Field to know if the product is active or not active"))
    
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        """Return title of product."""
        return self.title

    def get_absolute_url(self):
        return reverse("shop:detail", kwargs={'slug': self.slug})
    
    def get_price(self):
        return self.price
    
    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class OrderItem(models.Model):
    """
    This model is the relation between the producto and the order.
    """
    order = models.ForeignKey("Order", verbose_name = _('Order'), related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name = _('Product'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name = _('Quantity'), default = 1, help_text=_("Quantity you want to buy"))
    
    class Meta:
        verbose_name = _('OrderItem')
        verbose_name_plural = _('OrderItems')

    def __str__(self):
        """ Return quantity and title of product"""
        return f"{self.quantity} x {self.product.title}"
    
    def get_raw_total_item_price(self):
        return self.quantity * self.product.price
    
    def get_total_item_price(self):
        price = self.get_raw_total_item_price() 
        return price
    
class Order(models.Model):
    """
    This class allows you to purchase a product, related to, model: `auth.User`.
    """
    user = models.ForeignKey(User, verbose_name = _('User'), on_delete=models.CASCADE, blank=True, null=True, help_text=_("Name of the user making the purchase "))
    start_date = models.DateTimeField(verbose_name = _('Start date'), auto_now_add=True, blank=True)
    ordered_date = models.DateTimeField(verbose_name = _('Ordered date'), blank=True, null=True, help_text=_("Date of purchase"))
    ordered = models.BooleanField(verbose_name = _('Ordered'), default=False)
    billing_address = models.ForeignKey(
        Address, 
        verbose_name = _('Billing address'), 
        related_name='billing_address', 
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL)
    shipping_address = models.ForeignKey(
        Address, 
        verbose_name = _('Shipping address'),
        related_name='shipping_address', 
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        """Return reference number of the order"""
        return self.reference_number

    @property
    def reference_number(self):
        return f"ORDER-{self.pk}"
    
    def get_raw_subtotal(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_raw_total_item_price()
        return total

    def get_subtotal(self):
        subtotal = self.get_raw_subtotal()
        return subtotal

    def get_raw_total(self):
        subtotal = self.get_raw_subtotal()
        # agregar suma de IGV, Delivery, Resta DESCUENTOS
        #total = subtotal - discounts + tax + delivery
        return subtotal

    def get_total(self):
        total = self.get_raw_total()
        return total
    
class Payment(models.Model):
    """
    This class allows you to make a payment for an order.
    """
    order = models.ForeignKey(Order, verbose_name = _('Order'), on_delete=models.CASCADE, related_name='payments')
    full_name = models.CharField(verbose_name=_('Full name'),max_length=100)
    email = models.EmailField(verbose_name=_('Email'),max_length=254, blank=True)
    address1 = models.CharField(verbose_name=_('Address 1'),max_length=250)
    city = models.CharField(verbose_name=_('City'),max_length=100)
    postal_code = models.CharField(verbose_name=_('postal code'),max_length=20)
    country_code = models.CharField(verbose_name=_('Country code'),max_length=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(verbose_name=_('Total Pay'),max_digits=5, decimal_places=2)
    order_key = models.CharField(verbose_name=_('Order key'),max_length=200)
    payment_option = models.CharField(verbose_name=_('Payment option'),max_length=200)
    billing_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def __str__(self):
        return self.reference_number

    @property
    def reference_number(self):
        return f"PAYMENT-{self.order}-{self.pk}"

def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_product_receiver, sender=Product)