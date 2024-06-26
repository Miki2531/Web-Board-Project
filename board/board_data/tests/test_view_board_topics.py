from django.contrib.auth.models import User
from django.urls import reverse
from django.urls import resolve
from django.test import TestCase
from ..views import board_topics, TopicListView
from ..models import Board
from ..forms import NewTopicForm 



class BoardTopicsTest(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', descriptions='Django board')

    def test_board_topic_views_success_status_code(self):
        url= reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 20})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)


    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, TopicListView)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

class LoginRequiredNewTopic(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django Board')
        self.url = reverse('new_topic', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))