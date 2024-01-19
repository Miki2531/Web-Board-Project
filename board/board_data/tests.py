from django.contrib.auth.models import User
from django.urls import reverse
from django.urls import resolve
from django.test import TestCase
from .views import home, board_topics, new_topic
from .models import Board, Topic, Post
from .forms import NewTopicForm

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



class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', descriptions='Django board')
        User.objects.create_user(username='miko', email='miko@gmail.com', password='123')


    def test_csrf(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'New title',
            'message': 'Django discussion'
        }

        response= self.client.get(url, data)
        #self.assertTrue(Topic.objects.exists())
        #self.assertTrue(Post.objects.exists())

    
    def test_contains_forms(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    
    def test_new_topic_invalid_post_data(self):
        """
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        """

        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url)
        # form = response.context.get('form')
        self.assertEquals(response.status_code, 302)
        # self.assertTrue(form.errors)

    def test_new_topic_invalid_post_data_empty_fields(self):
        '''
           Invalid post data should not redirect
           The expected behavior is to show the form again with validation errors
        '''
         
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
             'subject': '',
             'message': ''
         }
        
        response = self.client.get(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_new_topic_view_success_status_code(self):
        # check if the request to the view is successful.
        url = reverse('new_topic', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topics_not_found_status_code(self):
        # check if the view is raising a 404 error when the Board does not exist.
        url = reverse('new_topic', kwargs={'pk': 90})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolve_new_topic_view(self):
        # check if the right view is being used.
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_contains_navigation_links(self):
        # ensure the navigation back to the list of topics.
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})

        response = self.client.get(board_topics_url)

        self.assertContains(response, 'href="{0}"'.format(new_topic_url)) 
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

