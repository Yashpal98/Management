from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

def admin(request):
    return render(request, 'admin-login/login.html')

def handleSignin(request):
    if request.method == 'POST':
        loginusername = request.POST["username"]
        loginpass = request.POST['password']
        user = authenticate(username=loginusername, password=loginpass)
        if user is not None:
            login(request, user)
            return render(request, 'admin-login/home.html')
        else:
            return redirect('admin_login')
    return HttpResponse("404 - Not Found")
    