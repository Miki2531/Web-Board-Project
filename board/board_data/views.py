from django.contrib.auth.models import User
from django.shortcuts import render, redirect,  get_object_or_404
from .models import Board, Topic, Post

# Create your views here.

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})
    

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    context = {'board': board}
    return render(request, 'topics.html', context)


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)


    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']


        user = User.objects.first()

        topic = Topic.objects.create(
            subject=subject,
            board = board,
            starter = user
        )

        post = Post.objects.create(
            message=message,
            topic = topic,
            created_by = user
        )

        return redirect('board_topics', pk=board.pk)

    context = {'board': board}
    return render(request, 'new_topic.html', context)







    

