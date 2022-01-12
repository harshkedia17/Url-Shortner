from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib import messages
# Create your views here.




def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST['username'] and request.POST['password']:
                username = request.POST.get('username')
                password = request.POST.get('password')
                try:
                    user = User.objects.get(username=username)

                except User.DoesNotExist:
                    return render(request, 'login.html', {'error': 'User Does Not Exist'})

                user = authenticate(request, username=username, password=password)

                if user is not None:
                    auth_login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'login.html', {'error': 'Username or Password is Incorrect'})
            else:
                return render(request, 'login.html', {'error': 'Empty Fields'})
        return render(request, 'login.html')
    else:
        return redirect('/')

def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password2']:
            if request.POST['username'] and request.POST['email'] and request.POST['password']:
                try:
                    user = User.objects.get(email=request.POST['username'])
                    return render(request, 'signup.html', {'error': "User already exists"})
                except User.DoesNotExist:
                    User.objects.create_user(
                        username=request.POST['username'],
                        email=request.POST['email'],
                        password=request.POST['password']
                    )
                    messages.success(
                        request, "Signup Succesful \n  Login here")
                    return redirect(login)

            else:
                return render(request, 'signup.html', {'error': "Empty Fields"})
        else:
            return render(request, 'signup.html', {'error': "Password's dont match"})

    return render(request, 'signup.html')


def logout(request):
    auth_logout(request)
    return render(request, 'home.html')
