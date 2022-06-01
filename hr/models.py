from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Interview(models.Model):
    interviewDate = models.DateField(
        verbose_name = _('Inteview date'),
        help_text=_("Enter the interview date "))
    interviewFile = models.CharField(
        verbose_name = _('Interview file'),
        max_length=250, 
        help_text=_("Add interview file"))
    interviewPerformance = models.BooleanField(
        verbose_name = _('Interview performance'),
        default = False,
        help_text=_("Interview performance OK?"))
    interviewResults = models.CharField(
        verbose_name = _('Interview results'),
        max_length=250,
        help_text=_("Enter the interview results"))
    location = models.CharField(
        verbose_name = _('Location'),
        max_length=250,
        help_text=_("Enter Location"))

    class Meta:
        verbose_name = _('Interview')
        verbose_name_plural = _('Interviews')

class Area(models.Model):
    """
    In this model the departments that the organization owns are created.
    """

    areaName = models.CharField(
        verbose_name = _('Area name'),
        max_length=250, 
        help_text=_("Enter the area name"))
    areaDescription = models.CharField(
        verbose_name = _('Area description'),
        max_length=500, 
        help_text=_("Enter the area description"))
    areaCode = models.CharField(
        verbose_name = _('Area Code'),
        max_length=250, 
        help_text=_("Enter area code"))

    class Meta:
        verbose_name = _('Area')
        verbose_name_plural = _('Areas')

    def __str__(self):
        """Return area name"""
        return self.areaName

class JobDescription(models.Model):
    """
    In this model the job descriptions to be used for recruitments are created.

    Stores a Job Description entry, related to :model:`auth.User` and :model:`hr.Area`.  
    """

    createdBy = models.ForeignKey(
        User,
        verbose_name = _('Created by'),
        null=False, 
        on_delete=models.CASCADE,
        help_text=_("User who created the description."))
    creationDate = models.DateField(
        verbose_name = _('Creation date'),
        help_text=_("Creation date for job description"))
    code = models.CharField(
        verbose_name = _('Code'),
        max_length=250, 
        help_text=_("Enter the code"))
    title = models.CharField(
        verbose_name = _('Title'),
        max_length=250, 
        help_text=_("Enter the title"))
    departament = models.ForeignKey(
        Area,
        null=False,
        on_delete=models.CASCADE,     
        verbose_name = _('Departament'),
        help_text=_("Enter the departament"))
    reportTo = models.CharField(
        verbose_name = _('Report to'),
        max_length=250, 
        help_text=_("Enter report to"))
    jobDescription = models.CharField(
        verbose_name = _('Job description'),
        max_length=500, 
        help_text=_("Enter job description"))
    responsabilities = models.CharField(
        verbose_name = _('Responsabilities'),
        max_length=500, 
        help_text=_("Enter the responsabilities"))
    skills = models.CharField(
        verbose_name = _('Skills'),
        max_length=500, 
        help_text=_("Enter the skills"))
    abilities = models.CharField(
        verbose_name = _('Abilities'),
        max_length=250,
        help_text=_("Enter the abilities"))
    experience = models.CharField(
        verbose_name = _('Experience'),
        max_length=250,
        help_text=_("Enter the Experience"))
    educationRequirements = models.CharField(
        verbose_name = _('Education requirements'),
        max_length=250,
        help_text=_("Enter the education requirements"))
    knowledge = models.CharField(
        verbose_name = _('Knowledge'),
        max_length=250,
        help_text=_("Enter the knowledges"))
    annualSalary = models.DecimalField(
        verbose_name = _('Annual salary'), 
        default = 0,
        decimal_places = 2,
        max_digits = 11,
        help_text=_("Enter annual salary in USD"))

    class Meta:
        verbose_name = _('Job description')
        verbose_name_plural = _('Job descriptions')

    def __str__(self):
        """Return code job description"""
        return self.code

class Recruitment(models.Model):
    """  
    Recruitment applications are created in this model.
    
    Stores a Recruitment entry, related to :model:`auth.User`, :model:`hr.JobDescription` and :model:`hr.Area`. 
    """

    requester = models.ForeignKey(
        User,
        verbose_name = _('Requester'),
        null=False, 
        on_delete=models.CASCADE,
        help_text=_("Requester who created the request."))
    dateOfRequest = models.DateField(
        verbose_name = _('Date of request'),
        help_text=_("Date of request recruitment"))
    departament = models.ForeignKey(
        Area,
        null=False,
        on_delete=models.CASCADE,     
        verbose_name = _('Departament'),
        help_text=_("Enter the departament"))
    jobDescription = models.ForeignKey(
        JobDescription,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name = _('Job description'),
        help_text=_("Select job description"))
    startingDate = models.DateField(
        verbose_name = _('Starting date'),
        help_text=_("Starting date"))
    numberOfVacancies = models.PositiveIntegerField(
        verbose_name = _('Number of vacancies'),
        help_text=_("Enter the number of vacancies"))
    title = models.CharField(
        verbose_name = _('Title'),
        max_length=250, 
        help_text=_("Enter the title"))
    responsabilities = models.CharField(
        verbose_name = _('Responsabilities'),
        max_length=500, 
        help_text=_("Enter the responsabilities"))
    location = models.CharField(
        verbose_name = _('Location'),
        max_length=250, 
        help_text=_("Enter location"))
    comments = models.CharField(
        verbose_name = _('Comments'),
        blank=True,
        max_length=500, 
        help_text=_("Enter the comments"))
    requisitionApproved = models.BooleanField(
        verbose_name = _('Requisition approved?'), 
        default=False,
        help_text=_("Requisition Approved?"))
    approvalsComments = models.CharField(
        verbose_name = _('Approvals comments'),
        blank=True,
        max_length=500, 
        help_text=_("Enter the comments"))

    class Meta:
        verbose_name = _('Recruitment')
        verbose_name_plural = _('recruitments')

    def __str__(self):
        """Return title of recruitment"""
        return self.title