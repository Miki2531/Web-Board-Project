from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.test import TestCase
from django.urls import reverse
from django.urls import resolve
from .views import signup


class signUpTestCase(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolve_signup_views(self):
        view = resolve('/signup/').func
        self.assertEquals(view, signup)
    
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)


    def test_forms_input(self):
        '''
        The view must contain five inputs: csrf, username, email,
        password1, password2
        '''
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):

    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'username',
            'email': 'mik@gmail.com',
            'password1': 'password12345',
            'password2': 'password12345'
        }

        self.response  = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirection(self):
        """
        Test a valid form submission should be redirected to the user home page.
        
        """
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exist())

    def test_user_is_authenticated(self):
        """
        create a request to arbitirary page.
        The resulting response should now have 'user' it is context, after success full signup.
        """

        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url, {})

    def test_signup_status_code(self):
        """
        Invalid ssubmitted form redirected to the home page.
        """

        self.assertEquals(self.response.status_code, 200)


    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_creat_user(self):
        self.assertFalse(User.objects.exists())








