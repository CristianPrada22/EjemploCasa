from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Person(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name = _('User'),
        null=True,
        blank=True, 
        on_delete=models.CASCADE,
        help_text=_("Enter a user name"))
    cc = models.CharField(
        verbose_name = _('CC'),
        max_length=11, 
        blank=True, 
        help_text=_("Enter your ID number"))
    name = models.CharField(
        verbose_name = _('Name'),
        max_length=50, 
        blank=True, 
        help_text=_("Enter your name"))
    lastName = models.CharField(
        verbose_name = _('Last name'),
        max_length=50, 
        blank=True, 
        help_text=_("Enter your last name"))
    email = models.CharField(
        verbose_name = _('E-mail'),
        max_length=100, 
        blank=True, 
        help_text=_("Enter your e-mail"))
    cv = models.FileField(
        verbose_name = _('CVs'),
        blank=True,
        upload_to='CVs'
    )
    cellphone = models.CharField(
        verbose_name = _('Cellphone'),
        max_length=11, 
        blank=True, 
        help_text=_("Enter your cell phone number"))
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
        return self.name +" "+ self.lastName 

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons') 

class Role(models.Model):
    name = models.CharField(
        verbose_name = _('Name'),
        max_length=50, 
        blank=True, 
        help_text=_("Enter the role name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

class PersonRole(models.Model):
    person = models.ForeignKey(
        Person,
        verbose_name = _('Person'),
        null=True,
        blank=True, 
        on_delete=models.CASCADE,
        help_text=_("Role holder"))
    role = models.ForeignKey(
        Role,
        verbose_name = _('Role'),
        null=True,
        blank=True, 
        on_delete=models.CASCADE,
        help_text=_("Assigned role"))
    dateCreated = models.DateTimeField(
        verbose_name = _('Date created'), 
        auto_now_add=True)
    active = models.BooleanField(
        verbose_name = _('Active'), 
        default=False, 
        help_text=_("Field to know if the role is active or not active"))

    class Meta:
        verbose_name = _('Person-Role')
        verbose_name_plural = _('Persons-Roles')