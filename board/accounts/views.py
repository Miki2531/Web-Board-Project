from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm

def login_views(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, 'user name does not exists.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'home')
        else:
            messages.error(request, 'Username or password is incorrect!!')

    context = {'page': page}
    return render(request, 'login.html', context)




def logout_views(request):
    logout(request)
    return redirect('home')



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else: 
        form = SignUpForm()
    context = {'form': form}
    return render (request, 'signup.html', context)

