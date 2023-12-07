from django.urls import path
from . import views


urlpatterns = [
    path('boards/', views.board_list, name='board_list'),
    path('boards/<int:board_id>/topics/<int:topic_id>/', views.topic_posts, name='topic_posts'),
]