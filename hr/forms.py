from tabnanny import verbose
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

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