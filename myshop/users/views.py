from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import CustomSignupForm, LoginForm

# Create your views here.


# signup page
def user_signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:index')
    else:
        form = CustomSignupForm()
    return render(request, 'users/register.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('store:index')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')