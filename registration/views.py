from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Comment

# Create your views here.
def loginPage(request):

    if request.user.is_authenticated:
        return redirect('index')

    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')

            else: 
                messages.error(request, 'Username or Password is incorrect.')

        context = {}
        return render(request, 'registration/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, "Account is successfully created.")
                return redirect('login')

        
        context = {'form': form}
        return render(request, 'registration/signup.html', context)

@login_required(login_url='login')
def index(request):

    if request.method == 'POST':
        form = CommentForm(request.POST)
        username = request.user.get_username()
        comment = request.POST.get('text')
        print("{}:{}".format(username, comment))
        new = Comment(name=username, text=comment)
        new.save()

    else: 
        form = CommentForm()

    
    count = Comment.objects.count()
    print(count,type(count))

    if count < 1:
        messages.info(request, "no feedback yet....")

    comments = Comment.objects.order_by('-date_added')
    context = {'comments': comments, 'form': form}
    return render(request, 'registration/index.html', context)


