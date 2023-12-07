from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *

# Create your views here.

def board_list(request):
    boards = Board.objects.all()
    context = {'boards': boards}
    return render(request, 'home.html', context)


def topic_posts(request, board_id, topic_id):
    board = get_object_or_404(Board, id=board_id)
    topic = get_object_or_404(Topic, id=topic_id, board=board)
    posts = topic.posts.all()
    return render(request, 'topic_posts.html', {'board': board, 'topic': topic, 'posts': posts})


    

