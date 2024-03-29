from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm 
from django.contrib.auth.models import User
from django.core import mail
from django.urls import resolve, reverse
from django.test import TestCase


class PasswordResetTeset(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)


    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contain_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_form_inputs(self):
        """The view contain two inputs: csrf and email"""
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)

class SuccessfulPasswordResetTest(TestCase):
    def setUp(self):
        email = 'miko@gmail.com'
        User.objects.create_user(username='miko', email=email, password='miko123')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_redirection(self):
        """A valid form submission should redirect the user to `password_reset_done` view"""
        url = reverse('password_reset')
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))

class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'donotexist@email.com'})

    def test_redirection(self):
        """
        Invalid email in the database should be redirect the user to `password_reset_done` view
        """
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_no_reset_email_sent(self):
        self.assertEqual(0, len(mail.outbox))


class PasswordResetDoneTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/reset/done/')
        self.assertEquals(view.func.view_class, auth_views.PasswordChangeDoneView)