from django.test import TestCase, Client
from hr.models import *
from django.urls import reverse

class TestHrViews(TestCase):
    """ Test for Views """
    fixtures = ['hr/fixtures/dev.json','main/fixtures/dev.json',]

    """ Test View - JobDescription View """
    def test_job_description_GET(self):

        client = Client()
        response = client.get(reverse('hr:jobDescription'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'jobDescription.html')

    """ Test View - ApproveRequest View """
    def test_approve_request_GET(self):
        client = Client()
        response = client.get(reverse('hr:approveRequest'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'approveRequest.html')

    """ Test View - Recruitment View """
    def test_recruitment_request_GET(self):

        client = Client()
        response = client.get(reverse('hr:recruitment'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'recruitmentRequest.html')    