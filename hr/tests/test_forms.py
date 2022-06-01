from django.test import TestCase
from hr.forms import *

class TestJobDescriptionForm(TestCase):
    """ Test for JobDescription form """

    def Mytest(self):
        form_data = {
            "createdBy": "1",
            "creationDate": "2022-02-09",
            "code": "HR_oficcer",
            "title": "Human Resources officer",
            "departament": "2",
            "reportTo": "Olga Lucero Vega",
            "jobDescription": "Develop and implement policies related to the effectiveness of the organization's personnel.",
            "responsabilities": "Promote company values such as equality and diversity, manage payroll, interpret employment laws, dealing with grievances and implementing disciplinary files.",
            "skills": "Leadership",
            "abilities": "Leadership",
            "experience": "2 years",
            "educationRequirements": "High School",
            "knowledge": "Labor law, Personnel management.",
            "annualSalary": "500"
        }
        form = AddJobDescriptionForm(data=form_data)
        self.assertTrue(form.is_valid())
            

class TestRecruitment(TestCase):
    """ Test for Recruitment model """

    def Mytest(self):
        form_data = {
            "requester": "1",
            "dateOfRequest": "2022-02-09",
            "startingDate": "2022-02-09",
            "title": "Recruitment Researcher",
            "departament": "2",
            "location": "Villavicencio",
            "jobDescription": "4",
            "responsabilities": "Search and recruit qualified personnel.",
            "numberOfVacancies": "5",
            "comments": "none",
            "requisitionApproved": "False",
            "approvalsComments": ""
        }
        form = AddRecruitmentForm(data=form_data)
        self.assertTrue(form.is_valid())
