from tabnanny import verbose
from django import forms
from django.forms import fields
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from shop.models import OrderItem, Address
User = get_user_model()

#contact form class
class Contactf(forms.Form):
    Name = forms.CharField(label = _('Name'), 
        max_length=100, 
        widget=forms.TextInput(attrs={ 'placeholder': _("Your Name")
    }))
    Last_name = forms.CharField(label = _('Last name'),
        max_length=100, 
        widget=forms.TextInput(attrs={ 'placeholder': _("Your Last Name")
    }))
    Email = forms.EmailField(label = _('Email'), 
        widget=forms.TextInput(attrs={ 'placeholder': _("Your e-mail")
    }))
    Message = forms.CharField(label = _('Message'),
        widget=forms.Textarea(attrs={ 'placeholder': _("Your Message")
    }))

class AddToCartForm(forms.ModelForm):

    class Meta:
        model = OrderItem
        fields = ['quantity']
        help_texts = {'quantity': None,}
        verbose_name = _('quantity')

class AddressForm(forms.Form):
    
    shipping_address_line_1 = forms.CharField(required=False, widget = forms.TextInput(attrs={'class': 'form-control',}))
    shipping_zip_code = forms.CharField(required=False, widget = forms.TextInput(attrs={'class': 'form-control',}))
    shipping_city = forms.CharField(required=False, widget = forms.TextInput(attrs={'class': 'form-control',}))

    billing_address_line_1 = forms.CharField(required=False, widget = forms.TextInput(attrs={'class': 'form-control',}))
    billing_zip_code = forms.CharField(required=False, widget = forms.TextInput(attrs={'class': 'form-control',}))
    billing_city = forms.CharField(required=False, widget = forms.TextInput(attrs={'class': 'form-control',}))

    selected_shipping_address = forms.ModelChoiceField(
        Address.objects.none(), required=False,
        widget = forms.Select(attrs={'class': 'form-control',})
    )

    selected_billing_address = forms.ModelChoiceField(
        Address.objects.none(), required=False,
        widget = forms.Select(attrs={'class': 'form-control',})
    )

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        super().__init__(*args, **kwargs)

        user = User.objects.get(id=user_id)

        shipping_address_qs = Address.objects.filter(
            user=user,
            address_type='S'
        )

        billing_address_qs = Address.objects.filter(
            user=user,
            address_type='B'
        )

        self.fields['selected_shipping_address'].queryset = shipping_address_qs
        self.fields['selected_billing_address'].queryset = billing_address_qs


    def clean(self):
        data = self.cleaned_data

        selected_shipping_address = data.get('selected_shipping_address', None)
        if selected_shipping_address is None:
            if not data.get('shipping_address_line_1', None):
                self.add_error("shipping_address_line_1", "Please fill in this field")
            if not data.get('shipping_zip_code', None):
                self.add_error("shipping_zip_code", "Please fill in this field")
            if not data.get('shipping_city', None):
                self.add_error("shipping_city", "Please fill in this field")

        selected_billing_address = data.get('selected_billing_address', None)
        if selected_billing_address is None:
            if not data.get('billing_address_line_1', None):
                self.add_error("billing_address_line_1", "Please fill in this field")
            if not data.get('billing_zip_code', None):
                self.add_error("billing_zip_code", "Please fill in this field")
            if not data.get('billing_city', None):
                self.add_error("billing_city", "Please fill in this field")
