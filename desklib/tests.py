from django.test import TestCase
from django.urls import reverse
from rest_framework import status

# Create your tests here.
from subjects.models import Subject
from documents.models import Document
from homework_help.models import Question, Answers
from subscription.models import Subscription


class TestCalls(TestCase):
    def test_call_view_working_successfully(self):
        response = self.client.get(reverse('home'))
        response.content
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('study:study-search'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('writing:writing'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('writing:compare'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('writing:grammar'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('writing:sample-list-view'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('homework_help:ask-question-view'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('documents:document-view', kwargs={'slug': "propertyreport-5-fdedeh"}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('subjects:subjects'))
        self.assertEqual(response.status_code, 200)

    def test_signup_form_submit(self):
        response = self.client.post(reverse('account_signup'), {}) # blank data dictionary
        self.assertFormError(response, 'form', 'email', 'This field is required.')
        response = self.client.post(reverse('account_signup'), {'email': 'sfafd@fsdfsd.sdfsdf', 'password1': 'locus123', 'password2': 'locus123'})
        self.assertFormError(response, 'form', 'first_name', 'This field is required.')
        response = self.client.post(reverse('account_signup'), {'email': 'test@test.test', 'first_name': 'test', 'last_name': 'test', 'contact_no': '+91-9582936122', 'password1': 'locus123', 'password2': 'locus123'})
        self.assertEqual(response.status_code, 200)

    def test_login_form_submit(self):
        self.client.login(username='user', password='test')
        response = self.client.post(reverse('account_login'), {}) # blank data dictionary
        self.assertFormError(response, 'form', 'login', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')
        response = self.client.post(reverse('account_signup'), {'login': 'test@test.test', 'password': 'locus123'})
        self.assertEqual(response.status_code, 200)


class SubjectModelTest(TestCase):

    def setUp(self):
        self.subject1 = Subject.objects.create(name='subject 1', slug='subject-1', description='this is for testing')

    def test(self):
        self.assertEquals(self.subject1.slug, 'subject-1')


class QuestionModelTest(TestCase):

    def setUp(self):
        self.question1 = Question.objects.create(question='hsgsh gkjhfkjgh kjhfgjk dfhkgjh dfjk hgkjdfhgk jdfhgj hdfgh')
        self.question1.slug = 'question-1'
        self.question1.save()

    def test(self):
        self.assertEquals(self.question1.slug, 'question-1')


class AnswerModelTest(TestCase):

    def setUp(self):
        self.question1 = Question.objects.create(question='hsgsh gkjhfkjgh kjhfgjk dfhkgjh dfjk hgkjdfhgk jdfhgj hdfgh')
        self.answer1 = Answers.objects.create(solution='this is a test answer', question=self.question1)

    def test(self):
        self.assertEquals(self.answer1.solution, 'this is a test answer')


class DocumentModelTest(TestCase):

    def setUp(self):
        self.document1 = Document.objects.create(upload_file='document/2020/05/11/190302637925517docx-1748_5kJgYpQ.docx')
        self.document1.slug = 'document-1'
        self.document1.save()

    def test(self):
        self.assertEquals(self.document1.slug, 'document-1')


    #
    #
    # def test_call_view_load(self):
    #     self.client.login(username='user', password='test')  # defined in fixture or with factory in setUp()
    #     response = self.client.get('/url/to/view')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'conversation.html')
    # def test_call_view_fail_invalid(self):
    #     # as above, but with invalid rather than blank data in dictionary
    #
    # def test_call_view_success_invalid(self):
    #     # same again, but with valid data, then
    #     self.assertRedirects(response, '/contact/1/calls/')
