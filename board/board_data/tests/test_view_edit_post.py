from django.forms import ModelForm
from django.contrib.auth.models import User
from django.test import testcases
from django.urls import resolve, reverse

from ..models import Board, Post, Topic
from ..views import PostUpdateView


class PostUpdateViewTestCase(testcases):
    '''
    Base test case to be used in all ``PostUpdateView view tests
    '''

    def setUp(self):
        self.board = Board.objects.create(name='Django', descriptions='Django board')
        self.username = 'miko'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='miko@gmail.com', password=self.password)
        self.topic = Topic.objects.create(subject='Hello world', board=self.board, starter=user)
        self.post = Post.objects.create(message='Lorem ipsum dolor sit amet', topic = self.topic, created_by= user )
        self.url = reverse('edit_post', kwargs={
            'pk': self.board,
            'topic_pk': self.topic.pk,
            'post_pk': self.post.pk
        })

class LoginRequiredPostUpdateViewTests(PostUpdateViewTestCase):
    def login_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))

class UnauthorizedPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        username = 'dani'
        password = '345'
        user = User.objects.create_user(username=username, email='dani@gmail.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        '''
        A topic should be edit only by the owner.
        Unauthorized users should get 404 response( Page not Found)
        '''
        self.assertEquals(self.response.status_code, 303)

class PostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/boars/1/topics/1/posts/1/edit')
        self.assertEquals(view.func.view_class, PostUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_input(self):
        '''
        The view must contain the csrf, message textarea
        '''

        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)

class SuccessfulPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url,{'message':'Edited message'})

    def test_redirection(self):
        '''
        A valid form submission should redirect the user
        '''
        topic_post_url = reversed('topic_posts', kwargs={'pk':self.board.pk, 'topic_pk': self.topic.pk})
        self.assertRedirects(self.response, topic_post_url)

    def test_post_changed(self):
        self.post.refresh_from_db()
        self.assertEquals(self.post.message, 'edited message')


class InvalidPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        '''
        Submite an empty dictionary to the `reply_topic` view
        '''
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

