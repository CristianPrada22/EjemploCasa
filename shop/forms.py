import mercadopago
from django.conf import settings
from tabnanny import verbose
from django import forms
from django.forms import fields
from django.utils.translation import ugettext_lazy as _

from shop.models import OrderItem, Payment

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
        fields = [_('quantity')]
        help_texts = {'quantity': None,}
        verbose_name = _('quantity')

class PaymentForm(forms.ModelForm):
    token = forms.CharField()

    class Meta:
        model = Payment
        fields = [
            "transaction_amount",
            "installments",
            "payment_method_id",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        self.order = kwargs.pop("order")
        super().__init__(*args, **kwargs)

    def clean_transaction_amount(self):
        transaction_amount = self.cleaned_data["transaction_amount"]
        if float(transaction_amount) != float(self.order.get_total_price()):
            raise forms.ValidationError(
                "Transaction Amount does not match the database!"
            )
        return transaction_amount

    def save(self):
        cd = self.cleaned_data
        mp = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
        payment_data = {
            "transaction_amount": float(self.order.get_total_price()),
            "token": cd["token"],
            "description": self.order.get_description(),
            "installments": cd["installments"],
            "payment_method_id": cd["payment_method_id"],
            "payer": {
                "email": cd["email"],
                "identification":  cd["doc_number"],
            },
        }
        payment = mp.payment().create(payment_data)

        if payment["status"] == 201:
            self.instance.order = self.order
            self.instance.mercado_pago_id = payment["response"]["id"]
            self.instance.mercado_pago_status_detail = payment["response"][
                "status_detail"
            ]
            self.instance.mercado_pago_status = payment["response"]["status"]

            if payment["response"]["status"] == "approved":
                self.order.paid = True
                self.order.save()
            self.instance.save()


class UpdatePaymentForm(forms.Form):
    action = forms.CharField()
    data = forms.JSONField()

    def save(self):
        cd = self.cleaned_data
        mp = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
        if cd["action"] == "payment.updated":
            mercado_pago_id = cd["data"]["id"]
            payment = Payment.objects.get(mercado_pago_id=mercado_pago_id)
            payment_mp = mp.payment().get(mercado_pago_id)

            payment.mercado_pago_status = payment_mp["response"]["status"]
            payment.mercado_pago_status_detail = payment_mp["response"]["status_detail"]

            if payment_mp["response"]["status"] == "approved":
                payment.order.paid = True
            else:
                payment.order.paid = False

            payment.order.save()
            payment.save()