from django.test import TestCase
from hr.models import *
from django.contrib.auth.models import User

class TestArea(TestCase):
    """ Test for Area model """

    def setUp(self):
        """ Test Insert - Area model """

        Area.objects.create(
            id=1,
            areaName="La Torre Eiffel3​ (Tour Eiffel, en francés), inicialmente llamada Tour de 300 mètres \
                (Torre de 300 metros) los ingenieros ", 
            areaDescription="La Torre Eiffel3​ (Tour Eiffel, en francés), inicialmente llamada Tour de 300 \
                mètres (Torre de 300 metros) es una estructura de hierro pudelado diseñada inicialmente por \
                los ingenieros civiles Maurice Koechlin y Émile Nouguier y construida, tras el rediseño \
                estético de Stephen Sauvestre, por el ingeniero civil francés Alexandre Gustave Eiffel y \
                sus colaboradores", 
            areaCode="prueba_01" 
        )
        self.Area= Area.objects.get(areaCode='prueba_01')
        self.queryset = Area.objects.all()

    def test_query_Area(self):
        """ Test Read - Area model """

        Area= self.Area.areaCode
        self.assertEqual(Area, "prueba_01")

    def test_update_Area(self):
        """ Test Update - Area model """

        self.Area.areaCode = "prueba_1"
        self.Area.save()
        self.assertEqual(self.Area.areaCode, "prueba_1")

    def test_delete_Area(self):
        """ Test Delete - Area model """

        self.Area.delete()
        self.assertNotIn(self.Area, self.queryset)

class TestJobDescription(TestCase):
    """ Test for JobDescription model """

    fixtures = ['hr/fixtures/dev.json','main/fixtures/dev.json',]

    def setUp(self):
        """ Test Insert - Area model """
    
        JobDescription.objects.create(
            id=5,
            createdBy= User.objects.get(id=1), 
            creationDate="2022-02-09", 
            code="prueba_01",
            title = "Controller Finance",
            departament = Area.objects.get(id=1),
            reportTo = "Olga Lucero Vega",
            jobDescription = "Control and supervision of the economic management of the company.",
            responsabilities = "Prepare and monitor the annual budget, coordinate audits and communicate \
                the company's financial situation to senior management to facilitate financial decision \
                making.",
            skills = "Administration and Finance",
            abilities = "Administration and Finance",
            experience = "2 years",
            educationRequirements = "High School",
            knowledge = "Administration and Finance",
            annualSalary = 500
        )
        self.JobDescription= JobDescription.objects.get(code='prueba_01')
        self.queryset = JobDescription.objects.all()

    def test_query_JobDescription(self):
        """ Test Read - JobDescription model """

        JobDescription= self.JobDescription.code
        self.assertEqual(JobDescription, "prueba_01")

    def test_update_JobDescription(self):
        """ Test Update - JobDescription model """

        self.JobDescription.code = "prueba_1"
        self.JobDescription.save()
        self.assertEqual(self.JobDescription.code, "prueba_1")

    def test_delete_JobDescription(self):
        """ Test Delete - JobDescription model """

        self.JobDescription.delete()
        self.assertNotIn(self.JobDescription, self.queryset)

class TestRecruitment(TestCase):
    """ Test for Recruitment model """

    fixtures = ['hr/fixtures/dev.json','main/fixtures/dev.json',]

    def setUp(self):
        """ Test Insert - Area model """

        Recruitment.objects.create(
            id=2,
            requester = User.objects.get(id=1),
            dateOfRequest = "2022-02-09",
            departament = Area.objects.get(id=1),
            jobDescription = JobDescription.objects.get(id=1),
            startingDate = "2022-02-09",
            numberOfVacancies = "5",
            title = "Recruitment",
            responsabilities = "Search and recruit qualified personnel.",
            location = "Villavicencio",
            comments = "none",
            requisitionApproved = "False",
            approvalsComments = ""
        )
        self.Recruitment= Recruitment.objects.get(title="Recruitment")
        self.queryset = Recruitment.objects.all()

    def test_query_Recruitment(self):
        """ Test Read - Recruitment model """

        Recruitment= self.Recruitment.title
        self.assertEqual(Recruitment, "Recruitment")

    def test_update_Recruitment(self):
        """ Test Update - Recruitment model """

        self.Recruitment.title = "prueba_1"
        self.Recruitment.save()
        self.assertEqual(self.Recruitment.title, "prueba_1")

    def test_delete_Recruitment(self):
        """ Test Delete - Recruitment model """

        self.Recruitment.delete()
        self.assertNotIn(self.Recruitment, self.queryset)