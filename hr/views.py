from django.http import request
from django.shortcuts import get_object_or_404, reverse, redirect, render
from django.views import generic
from django.conf import settings 

from hr.forms import AddJobDescriptionForm, AddRecruitmentForm, ApproveRequestForm, AdvertisementForm, ReceiveCVsForm, SelectInitialCandidateForm
from hr.models import JobDescription, Recruitment, Advertisement
from user.models import Person


class RecruitmentView(generic.FormView):
    """
    The backend of the Recruitment template is implemented in this view.

    Display an individual :model:`hr.Recruitment`.

    **Template:**

    :template:`hr/recruitmentRequest.html`

    **get_success_url()**

    We return/render the template under the alias we passed as parameter.

    **form_valid()**

    Validate the form fields and save the changes.
    """
    form_class = AddRecruitmentForm
    template_name = "recruitmentRequest.html"

    def get_success_url(self):
        return reverse('hr:recruitment')

    def form_valid(self, form):
        recruitment = form.save(commit=True)
        user = self.request.user
        form.instance.user = user
        form.save()
        return super(RecruitmentView, self).form_valid(form)

class JobDescriptionView(generic.FormView):
    """
    The backend of the JobDescription template is implemented in this view.

    Display an individual :model:`hr.JobDescription`.

    **Template:**

    :template:`hr/jobDescription.html`

    **get_success_url()**

    We return/render the template under the alias we passed as parameter.

    **form_valid()**

    Validate the form fields and save the changes.
    """

    form_class = AddJobDescriptionForm
    template_name = "jobDescription.html"

    def get_success_url(self):
        return reverse('hr:jobDescription')

    def form_valid(self, form):
        job = form.save(commit=True)
        user = self.request.user
        form.instance.user = user
        form.save()
        return super(JobDescriptionView, self).form_valid(form)

class ApproveRequestView(generic.FormView):
    """
    The backend of the ApproveRequest template is implemented in this view.

    Display an individual :model:`hr.Recruitment`.

    **Template:**

    :template:`hr/approveRequest.html`

    **get_success_url()**

    We return/render the template under the alias we passed as parameter.

    **get_object()**

    we return an object from a query, if the record/object to query does not exist it \
        returns a 404 status code. 

    **form_valid()**
    
    Validate the form fields and save the changes.

    **get_context_data()**

    We obtain the queried object and assign it a context name to use it in the FrontEnd.
    """

    form_class = ApproveRequestForm
    template_name = "approveRequest.html"

    def get_success_url(self):
        return reverse('hr:approveRequest')
    
    def get_object(self):
        return get_object_or_404(Recruitment, id='1')

    def form_valid(self, form):
        recruitment = self.get_object()
        recruitment.requisitionApproved = form.cleaned_data['requisitionApproved']
        recruitment.approvalsComments = form.cleaned_data['approvalsComments']
        recruitment.save()
        return super(ApproveRequestView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ApproveRequestView, self).get_context_data(**kwargs)
        context['approveR'] = self.get_object()
        return context

class RequestListView(generic.ListView):
    template_name='requestList.html'
    model = Recruitment
    context_object_name = 'reqList'

class JobVacancyAdvertisementView(generic.FormView):
    """
    The backend of the JobVacancyAdvertisement template is implemented in this view.

    Display an individual :model:'hr.Recruitment' and :model: 'hr.Advertisement'

    **Template:**

    :template:`hr/jobVacancyAdvertisement.html`
    
    **get_success_url()**

    We return/render the template under the alias we passed as parameter.
    
    **get_object()**

    we return an object from a query, if the record/object to query does not exist it \
        returns a 404 status code. 

    **form_valid()**
    
    Validate the form fields and save the changes.

    **get_context_data()**
    
    We obtain the queried object and assign it a context name to use it in the FrontEnd.
    """

    form_class = AdvertisementForm
    template_name = "jobVacancyAdvertisement.html"

    def get_success_url(self):
        return reverse('hr:jobVacancy')
    
    def get_object(self):
        return get_object_or_404(Recruitment, id='1')

    def form_valid(self, form):
        advertisement = Advertisement()
        advertisement.closingDate = form.cleaned_data['closingDate']
        advertisement.companyDescription = form.cleaned_data['companyDescription']
        advertisement.contactDetails = form.cleaned_data['contactDetails']
        advertisement.idealCandidate = form.cleaned_data['idealCandidate']
        advertisement.jobDescription = form.cleaned_data['jobDescription']
        advertisement.jobTitle = form.cleaned_data['jobTitle']
        advertisement.location = form.cleaned_data['location']
        advertisement.salaryGuide = form.cleaned_data['salaryGuide']
        advertisement.comments = form.cleaned_data['comments']
        advertisement.advertisementType = form.cleaned_data['advertisementType']
        advertisement.save()
        return super(JobVacancyAdvertisementView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(JobVacancyAdvertisementView, self).get_context_data(**kwargs)
        context['JVA'] = self.get_object()
        return context    
    
class ReceiveCVsView(generic.FormView):
    """
    The backend of the ReceiveCVs template is implemented in this view.

    Display an individual :model:`user.Person`.

    **Template:**

    :template:`hr/receiveCVs.html`

    **get_success_url()**

    We return/render the template under the alias we passed as parameter.

    **form_valid()**
    
    Validate the form fields and save the changes.

    """
    
    form_class = ReceiveCVsForm
    template_name = "receiveCVs.html"

    def get_success_url(self):
        return reverse('hr:receiveCV')

    def form_valid(self, form):
        person = Person()
        person.name = form.cleaned_data['name']
        person.lastName = form.cleaned_data['lastName']
        person.cc = form.cleaned_data['cc']
        person.Age = form.cleaned_data['age']
        person.email = form.cleaned_data['email']
        person.cellphone = form.cleaned_data['cellphone']
        person.home_address = form.cleaned_data['homeAddress']
        person.cv = form.cleaned_data['cv']
        person.save()
        return super(ReceiveCVsView, self).form_valid(form)

class SelectInicialCandidatesView(generic.FormView):
    """
    The backend of the selectInicialCandidates template is implemented in this view.

    Display an individual :model:`hr.Recruitment`.

    **Template:**

    :template:`hr/selectInicialCandidates.html`

    **get_success_url()**

    We return/render the template under the alias we passed as parameter.

    **get_object()**

    we return an object from a query, if the record/object to query does not exist it \
        returns a 404 status code. 

    **form_valid()**
    
    Validate the form fields and save the changes.

    **get_context_data()**

    We obtain the queried object and assign it a context name to use it in the FrontEnd.
    """

    form_class = SelectInitialCandidateForm
    template_name = "selectInitialCandidate.html"

    def get_success_url(self):
        return reverse('hr:selectIC')
    
    def get_object(self):
        return get_object_or_404(Recruitment, id='1')

    def form_valid(self, form):
        recruitment = self.get_object()
        recruitment.changeInAdverstisement = form.cleaned_data['changeInAdverstisement']
        recruitment.save()
        return super(SelectInicialCandidatesView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SelectInicialCandidatesView, self).get_context_data(**kwargs)
        recruitment = self.get_object()
        context['selectIC'] = recruitment
        context['advertisement'] = Advertisement.objects.get(jobTitle="Django/Python Developer")
        context['candidates'] = Person.objects.all()
        context['jobD'] = JobDescription.objects.get(code=recruitment.jobDescription)
        return context