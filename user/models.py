from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Person(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name = _('User'), 
        default=1, 
        null=True, 
        on_delete=models.CASCADE,
        help_text=_("Enter a user name "))
    cc = models.CharField(
        verbose_name = _('CC'),
        max_length=11, 
        blank=True, 
        help_text=_("Enter your ID number "))
    cellphone = models.CharField(
        verbose_name = _('Cellphone'),
        max_length=11, 
        blank=True, 
        help_text=_("Enter your cell phone number "))
    home_address = models.CharField(
        verbose_name = _('Home address'),
        max_length=150, 
        blank=True, 
        help_text=_("Enter your home address"))
    Age=models.IntegerField(
        verbose_name = _('Age'),
        default=0,
        help_text=_("Enter your Age"))

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons') 