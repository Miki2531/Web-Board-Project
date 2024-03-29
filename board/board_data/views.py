from django.contrib.auth.models import User
from django.shortcuts import render, redirect,  get_object_or_404
from .forms import NewTopicForm
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
    user = User.objects.first()


    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()

            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = user
            )

        return redirect('board_topics', pk=board.pk)
    else:
        form = NewTopicForm()

    context = {'board': board, 'form': form}
    return render(request, 'new_topic.html', context)







    

