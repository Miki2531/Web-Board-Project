from django.contrib.auth.models import User
from django.urls import reverse
from django.urls import resolve
from django.test import TestCase
from ..views import home, BoardListView
from ..models import Board, Topic, Post
from ..forms import NewTopicForm   



class HomeTest(TestCase):
    def setUp(self):
       self.board = Board.objects.create(name='Django', descriptions='Django board')
       url = reverse('home')
       self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_home_url_resolve_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, BoardListView)

    def test_home_view_contains_link_to_topics_page(self):
        board_topic_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topic_url))