from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_view
from django.urls import resolve, reverse
from django.test import TestCase

class PasswordChangeTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='miko25', email='miko23@gmail.com', password='miko1234')
        url = reverse('password_change')
        self.client.login(username='miko25', password='miko1234')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolve_correct_view(self):
        view = resolve('/settings/password/')
        self.assertAlmostEquals(view.func.view_class, auth_view.PasswordChangeView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_forms(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordChangeForm)

    def test_form_inputs(self):
        """
        The views must contain four inputs: csrf, old_password, new_password, confirm_password
        """

        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="password"', 3)

class LoginRequiredPasswordChangeTest(TestCase):
    def test_redirection(self):
        url = reverse('password_change')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, '{login_url}?next={url}'.formate(login_url=login_url, url=url))

class PasswordChangeTestCase(TestCase):
    '''Base test case for form processing accepts a 'data' dict to POST the view'''
    def setUp(self, data={}):
        self.user = User.objects.create_user(username='miko', email='miko25@gmail.com', password='miko1234')
        self.url = reverse('password_change')
        self.client.login(username='miko', password='old_password')
        self.response = self.client.post(self.url, data)

class SuccessfulPasswordChangeTest(PasswordChangeTestCase):
    def setUp(self):
        super.setUp({
            'old_password': 'old_password',
            'new_password1' : 'new_password1',
            'new_password2' : 'new_password2',
        })

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('password_change_done'))

    def test_password_changed(self):
        '''
        refresh the user instance from the db to get the new password
        hash update by the change password view.
        '''
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_user_authentication(self):
        response = self.client.get(reverse('home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class InvalidPasswordChangeTest(PasswordChangeTestCase):
    def test_status_code(self):
        '''
        An invalid form submission should return to the home page.
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_not_change_password(self):
        '''
        refresh the user instance from the db to make sure, the password changes.
        '''

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))
