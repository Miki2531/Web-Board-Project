from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Board, Post, Topic
from ..forms import PostForm
from ..views import reply_topic


class ReplyTopicTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', descriptions='Django Board')
        user = User.objects.create_user(username='miko', email='miko@gmail.com', password='miko123')
        self.topic = Topic.objects.create(subject='Hello', board=self.board, starter=user)
        Post.objects.create(message='Lorem ipsum', topic=self.topic, created_by=user)
        self.url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic': self.topic.pk})


class LoginRequiredReplyTopicTests(ReplyTopicTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))

class ReplyTopicTest(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username='miko', password='miko123')
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_func(self):
        view = resolve('/boards/1/topics/reply/')
        self.assertEquals(view.func, reply_topic)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PostForm)

    def test_form_inputs(self):
        'The view must contain two inputs: csrf, message textarea'

        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)

class SuccessfulReplyTopicTest(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username='miko', password='miko123')
        self.response = self.client.login(self.url, {'message', 'hello world!'})

    def test_redirection(self):
        '''
        A valid form submission redirect to the user
        '''
        url = reverse('topic_posts', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        topic_posts_url = '{url}?page=1#2'.format(url=url)
        self.assertRedirects(self.response, topic_posts_url)

    def test_reply_created(self):
        """
        The total post count should be 2
        """
        self.assertEquals(Post.objects.count(), 2)

class InvalidReplyTopicTests(ReplyTopicTest):
    def setUp(self):
        '''
        Submite an empty dictionary to the 'reply_topic' view
        '''
        super().setUp()
        self.client.login(username='miko', password='mk1223')
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.content.get('form')
        self.assertTrue(form.errors)