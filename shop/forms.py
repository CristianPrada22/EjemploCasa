from tabnanny import verbose
from django import forms
from django.forms import fields
from django.utils.translation import ugettext_lazy as _

from shop.models import OrderItem

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