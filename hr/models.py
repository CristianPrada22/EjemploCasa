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
    In this model the departments/Area that the organization owns are created.
    """

    areaName = models.CharField(
        verbose_name = _('Area name'),
        max_length=250, 
        help_text=_("Department/Area name"))
    areaDescription = models.CharField(
        verbose_name = _('Area description'),
        max_length=500, 
        help_text=_("Description of the department/area"))
    areaCode = models.CharField(
        verbose_name = _('Area Code'),
        max_length=250, 
        help_text=_("Department/Area code"))

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
        help_text=_("User creating the job description"))
    creationDate = models.DateField(
        verbose_name = _('Creation date'),
        help_text=_("Creation date for job description"))
    code = models.CharField(
        verbose_name = _('Code'),
        max_length=250, 
        help_text=_("ID of the job description"))
    title = models.CharField(
        verbose_name = _('Title'),
        max_length=250, 
        help_text=_("Title/name of the job description"))
    departament = models.ForeignKey(
        Area,
        null=False,
        on_delete=models.CASCADE,  
        verbose_name = _('Departament'),
        help_text=_("Department/Area associated with the job description"))
    reportTo = models.CharField(
        verbose_name = _('Report to'),
        max_length=250, 
        help_text=_("Immediate supervisor associated with the job description"))
    jobDescription = models.CharField(
        verbose_name = _('Job description'),
        max_length=500, 
        help_text=_("Job description"))
    responsabilities = models.CharField(
        verbose_name = _('Responsabilities'),
        max_length=500, 
        help_text=_("Job functions"))
    skills = models.CharField(
        verbose_name = _('Skills'),
        max_length=500, 
        help_text=_("The capacities to perform tasks that you are developed"))
    abilities = models.CharField(
        verbose_name = _('Abilities'),
        max_length=250,
        help_text=_("Talents you are born with."))
    experience = models.CharField(
        verbose_name = _('Experience'),
        max_length=250,
        help_text=_("Time of experience on the job"))
    educationRequirements = models.CharField(
        verbose_name = _('Education requirements'),
        max_length=250,
        help_text=_("Level of education required"))
    knowledge = models.CharField(
        verbose_name = _('Knowledge'),
        max_length=250,
        help_text=_("Knowledge required for the job"))
    annualSalary = models.DecimalField(
        verbose_name = _('Annual salary'), 
        default = 0,
        decimal_places = 2,
        max_digits = 11,
        help_text=_("Approximate annual salary"))

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
        help_text=_("User who created the request"))
    dateOfRequest = models.DateField(
        verbose_name = _('Date of request'),
        help_text=_("Date of recruitment request"))
    departament = models.ForeignKey(
        Area,
        null=False,
        on_delete=models.CASCADE,
        verbose_name = _('Departament'),
        help_text=_("Department/Area that require the recruitment"))
    jobDescription = models.ForeignKey(
        JobDescription,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name = _('Job description'),
        help_text=_("Associated job description"))
    startingDate = models.DateField(
        verbose_name = _('Starting date'),
        help_text=_("Start date of the job"))
    numberOfVacancies = models.PositiveIntegerField(
        verbose_name = _('Number of vacancies'),
        help_text=_("Number of vacancies available"))
    title = models.CharField(
        verbose_name = _('Title'),
        max_length=250, 
        help_text=_("Name of vacancy"))
    responsabilities = models.CharField(
        verbose_name = _('Responsabilities'),
        max_length=500, 
        help_text=_("Job functions"))
    location = models.CharField(
        verbose_name = _('Location'),
        max_length=250, 
        help_text=_("Work location"))
    comments = models.CharField(
        verbose_name = _('Comments'),
        blank=True,
        max_length=500, 
        help_text=_("A maximum of 500 characters is allowed"))
    requisitionApproved = models.BooleanField(
        verbose_name = _('Requisition approved'), 
        default=False,
        help_text=_("Requisition Approved?"))
    approvalsComments = models.CharField(
        verbose_name = _('Approvals comments'),
        blank=True,
        max_length=500, 
        help_text=_("A maximum of 500 characters is allowed"))
    changeInAdverstisement = models.BooleanField(
        verbose_name = _('Change In Adverstisement Need?'), 
        default=False,
        help_text=_("Change In Adverstisement Need?"))

    class Meta:
        verbose_name = _('Recruitment')
        verbose_name_plural = _('recruitments')

    def __str__(self):
        """Return title of recruitment"""
        return self.title

class Advertisement(models.Model):
    """
    Model to obtain the data that will be used to generate the advertising of the vacancies. 
    """
    closingDate = models.DateField(
        verbose_name = _('Closing date'),
        help_text=_("Closing date for advertisement"))
    companyDescription = models.CharField(
        verbose_name = _('Company description'),
        max_length=500,
        help_text=_("Short description of the company"))
    contactDetails = models.CharField(
        verbose_name = _('Contact details'),
        max_length=250,
        help_text=_("The necessary information to contact the candidate"))
    idealCandidate= models.CharField(
        verbose_name = _('Ideal candidate'),
        max_length=250,
        help_text=_("The characteristics of the ideal candidate"))
    jobDescription = models.CharField(
        verbose_name = _('Job description'),
        max_length=500,
        help_text=_("Characteristics that describe the vacancy ")) 
    jobTitle = models.CharField(
        verbose_name = _('Job title'),
        max_length=250,
        help_text=_("Name of the vacancy"))
    location = models.CharField(
        verbose_name = _('Location'),
        max_length=250,
        help_text=_("Location of the vacancy"))
    salaryGuide = models.CharField(
        verbose_name = _('Salary guide'),
        max_length=250,
        help_text=_("Characteristics such as experience that help establish the salary"))
    comments = models.CharField(
        verbose_name = _('Comments'),
        max_length=500,
        help_text=_("Comment here some additional features to consider"))
    advertisementType = models.BooleanField(
        verbose_name = _('Advertisement type'),
        default = False,
        help_text=_("Internal(True) or External(False)?"))
    class Meta:
        verbose_name = _('Advertisement')
        verbose_name_plural = _('Advertisements')

    def __str__(self):
        """Return job title of advertisement"""
        return self.jobTitle