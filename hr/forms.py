from tabnanny import verbose
from tkinter import Widget
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from user.models import Person

from .models import JobDescription, Recruitment

class AddJobDescriptionForm(forms.ModelForm):
    """ Form creation - AddJobDescription Form """

    class Meta:
        """ AddJobDescription Form Inherits from the JobDescription model. """

        model = JobDescription
        fields = [
            _('createdBy'), 
            _('creationDate'), 
            _('code'),
            _('title'), 
            _('departament'), 
            _('reportTo'),
            _('jobDescription'), 
            _('responsabilities'), 
            _('skills'),
            _('abilities'),
            _('experience'),
            _('educationRequirements'),
            _('knowledge'),
            _('annualSalary')]
        help_texts = {'': None,}
        verbose_name = [
            _('Created by'), 
            _('Creation date'), 
            _('Code'), 
            _('Title'), 
            _('Departament'),
            _('Report to'),
            _('Job description'),
            _('Responsabilities'),
            _('Skills'),
            _('Abilities'),
            _('Experience'),
            _('Education requirements'),
            _('Knowledge'),
            _('Annual salary')]

class AddRecruitmentForm(forms.ModelForm):
    """ Form creation - AddRecruitment Form """
    
    class Meta:
        """ AddRecruitment Form Inherits from the Recruitment model. """

        model = Recruitment
        fields = [
            _('requester'), 
            _('dateOfRequest'), 
            _('departament'), 
            _('jobDescription'),
            _('startingDate'),
            _('numberOfVacancies'),
            _('title'),
            _('responsabilities'),
            _('location'),
            _('comments')]
        help_texts = {'requester': None,}
        verbose_name = [
            _('Requester'),
            _('Date of request'),
            _('Departament'),
            _('Job description'),
            _('Starting date'),
            _('Number of vacancies'),
            _('Title'),
            _('Responsabilities'),
            _('Location'),
            _('Comments')]

class ApproveRequestForm(forms.Form):
    """ Form creation - ApproveRequest Form """

    """ Options for RequisitionApproved field in the AddRecruitment Form. """
    REQUISITION_APPROVED_CHOICES = [
        ('True', _('Yes')),
        ('False', 'No'),
    ]   

    requisitionApproved = forms.ChoiceField(
        label = _('Requisition approved'),
        required = True, 
        widget = forms.RadioSelect,
        choices = REQUISITION_APPROVED_CHOICES,
    )
    approvalsComments = forms.CharField(
        label = _('Approvals comments'),
        max_length=500,
        required=False, 
        widget=forms.Textarea(attrs={ 'placeholder': _("Approvals comments")
    }))
    
    def clean_requisitionApproved(self):
        """ Validation for RequisitionApproved field in the AddRecruitment Form. """
        data = self.cleaned_data['requisitionApproved']
        if data == "False":
            raise ValidationError(_("Approval comments is required"), code = 'invalid')
        return data

class AdvertisementForm(forms.Form):
    """ Form creation - Advertisement Form """

    """ Options for Advertisement field in the AddAdvertisement Form. """
    ADVERTISEMENT_CHOICES = [
        ('True', _('Internal')),
        ('False', 'External'),
    ]

    advertisementType = forms.ChoiceField(
        label = _('Advertisement Type'),
        required = True, 
        widget = forms.RadioSelect,
        choices = ADVERTISEMENT_CHOICES,)

    closingDate = forms.DateField(
        label = _('Closing date'),
        required = True,
        widget = forms.DateInput(attrs = { 'placeholder': _("YYYY-MM-DD"), 'class': 'form-control'})
        )

    companyDescription = forms.CharField(
        label = _('Company description'),
        max_length = 500,
        required = False,
        widget = forms.Textarea(attrs = { 'placeholder': _("Enter your company description"), 'class': 'form-control', 'rows': '3'}))

    contactDetails = forms.CharField(
        label = _('Contact details'),
        max_length = 250,
        required = True,
        widget = forms.Textarea(attrs = { 'placeholder': _("Enter your contact details"), 'class': 'form-control', 'rows': '3'}))

    idealCandidate= forms.CharField(
        label = _('Ideal candidate'),
        max_length = 250,
        required = False,
        widget = forms.Textarea(attrs = { 'placeholder': _("Enter the characteristics of the ideal candidate "), 'class': 'form-control', 'rows': '3'}))

    jobDescription = forms.CharField(
        label = _('Job description'),
        max_length = 500,
        required = True,
        widget = forms.Textarea(attrs={ 'placeholder': _("Enter job description"), 'class': 'form-control', 'rows': '3'}))

    jobTitle = forms.CharField(
        label = _('Job title'),
        max_length = 250,
        required = True,
        widget = forms.TextInput(attrs={ 'placeholder': _("Enter job title"), 'class': 'form-control'}))

    location = forms.CharField(
        label = _('Location'),
        max_length = 250,
        required = True,
        widget = forms.TextInput(attrs = { 'placeholder': _("Enter work location"), 'class': 'form-control'}))

    salaryGuide = forms.CharField(
        label = _('Salary guide'),
        max_length = 250,
        required = True,
        widget = forms.Textarea(attrs = { 'placeholder': _("Enter salary guide"), 'class': 'form-control', 'rows': '3'}))

    comments = forms.CharField(
        label = _('Comments'),
        max_length = 500,
        required = False,
        widget = forms.Textarea(attrs = { 'placeholder': _("Enter aditional comments"), 'class': 'form-control', 'rows': '3'}))

    def clean_advertisementType(self):
        """ Validation for advertisementType field in the Advertisement Form. """
        data = self.cleaned_data['advertisementType']
        if data == "False":
            raise ValidationError(_("Company Description is required"), code = 'invalid')
        return data

class ReceiveCVsForm(forms.Form):
    """ Form creation - ApproveRequest Form """

    name = forms.CharField(
        label = _('Name'),
        max_length = 50,
        required = True,
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Enter your name")})
    )
    lastName = forms.CharField(
        label = _('Last Name'),
        max_length = 50,
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Enter your last name")})
    )
    cc = forms.CharField(
        label = _('CC'),
        max_length = 11,
        widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': _("Enter your #ID")})
    )
    email = forms.EmailField(
        label = _('E-mail'),
        max_length = 100,
        widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _("Enter your E-mail")})
    )
    cellphone = forms.CharField(
        label = _('Cellphone'),
        max_length = 11,
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Enter your cellphone")})
    )
    homeAddress = forms.CharField(
        label = _('Home address'),
        max_length = 150,
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Enter your home address")})
    )
    age = forms.CharField(
        label = _('Age'),
        max_length = 3,
        widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': _("Enter your age")})
    )
    cv = forms.FileField(
        widget = forms.FileInput(attrs={'class': 'form-control-file'})
    )
