from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Board, Post, Topic
from ..views import *

class TopicPostsTest(TestCase):
    def setUp(self):
        board = Board.objects.create(name='Django', descriptions = 'Django Board')
        user  = User.objects.create_user(username='miko', email='miko@gmail.com', password='miko123')
        topic = Topic.objects.create(subject ='Hello world!!', board = board, starter = user )
        Post.objects.create(message='Lorem ipsum', topic=topic, created_by=user)
        url = reverse('topic_posts', kwargs={'pk': board.pk, 'topic_pk': topic.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('board/1/topics/1')
        self.assertEquals(view.func, topic_posts)
