from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.urls import reverse

# Create your views here.


def login(request):
    #Checks if user is already logged or not.
    if not request.user.is_authenticated:
        # if not logged & request method is post.
        if request.method == "POST":
            # handles login if email & pswrd are provided.
            if request.POST['email'] and request.POST['password']:
                try:
                    usr = User.objects.get(email=request.POST['email'])
                    username = usr.username
                    password = request.POST['password'] 
                    # Authenticates the user with password.
                    user = auth.authenticate(request, username = username, password = password)
                    if user is not None:
                        auth.login(request, user)#logins the user
                        if request.POST['next'] != '':
                            return redirect(request.POST.get('next'))
                        else:
                            return redirect('/')
                    else:
                        messages.error(request, "You Entered Wrong password")
                        return redirect(reverse('account:login'))
                except User.DoesNotExist:
                    messages.info(request, "User Doesn't Exist")
                    return redirect(reverse('account:login'))
            else:
                messages.info(request, "Empty Fields")
                return redirect(reverse('account:login'))
        else:
            return render(request, 'account/login.html')
    else:
        return redirect('/')

# Signup for user account
def signup(request):
    #Checks if user is already logged or not.
    if not request.user.is_authenticated:
        # if not logged & request method is post.
        if request.method == "POST":
            # handles signup if pswrd1 & pswrd2 are same.
            if request.POST['password'] == request.POST['password2']:
                if request.POST['username'] and request.POST['email'] and request.POST['password']:
                    try:
                        # Checks for the user already exist or not.
                        user = User.objects.get(email=request.POST['email'])
                        messages.info(request, "User Already Exists")
                        return redirect(reverse('account:signup'))
                    except User.DoesNotExist:
                        # If user not exist, creates the user.
                        User.objects.create_user(
                            username=request.POST['username'],
                            email=request.POST['email'],
                            password=request.POST['password'],
                        )
                        messages.success(request, "Signup Successful, Login Here")
                        return redirect(reverse('account:login'))
                else:
                    messages.error(request, "Empty Fields")
                    return redirect(reverse('account:signup'))
            else:
                messages.error(request, "Password's Don't Match")
                return redirect(reverse('account:signup'))
        else:
            return render(request, 'account/signup.html')
    else:
        return redirect('/')

# logouts the user
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out.")
    return redirect(reverse('account:login'))