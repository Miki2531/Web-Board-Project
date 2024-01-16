from django.urls import reverse
from django.urls import resolve
from django.test import TestCase
from .views import home, board_topics
from .models import Board

class HomeTest(TestCase):
    def setUp(self):
       self.board = Board.objects.create(name='Django', descriptions='Django board')
       url = reverse('home')
       self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_home_url_resolve_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topic_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topic_url))




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
        self.assertEquals(view.func, board_topics)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))




