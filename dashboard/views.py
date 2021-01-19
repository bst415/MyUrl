#from django.http import  HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import user_urls, public_urls
import datetime
import random
import string

# Create your views here.

# if logged in redirects to dashboard else to login page.
@login_required(login_url='/account/login/')
def dashboard(request):
    usr = request.user
    urls = user_urls.objects.filter(user=usr).order_by('-url_date')
    return render(request,'dashboard/dashboard.html', {'urls': urls})

# Random generator function
def randomgen():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(6))

# Generates or shortens url
def generate(request):
    if request.method == "POST":
        original = request.POST['original']
        createdate = datetime.datetime.now()
        duration = request.POST['duration']
        if duration == '1 Hour':
            duration = datetime.datetime.now()+datetime.timedelta(hours=1)
        elif duration == '1 day':
            duration = datetime.datetime.now()+datetime.timedelta(days=1)
        elif duration == '1 Week':
            duration = datetime.datetime.now()+datetime.timedelta(days=7)
        elif duration == '1 Month':
            duration = datetime.datetime.now()+datetime.timedelta(days=31)
        elif duration == '1 Year':
            duration = datetime.datetime.now()+datetime.timedelta(days=365)
        else:
            duration = datetime.datetime.now()+datetime.timedelta(days=3650)
        
        expiry = duration
        
        # Executes if user is authenticated
        if request.POST['original'] and request.user.is_authenticated:
            usr = request.user
            if request.POST['title']:
                title = request.POST['title']
            else:
                title = "No Title"
            if not request.POST['short_char']:
                # Generates randomly if custum short char is not provided.
                generated = False
                while not generated:
                    short = randomgen()
                    # Check for generated char in user_urls table
                    check = user_urls.objects.filter(short_char=short)
                    if not check:
                        newurl = user_urls(
                            user=usr,
                            title=title,
                            original_url=original,
                            short_char=short,
                            url_date=createdate,
                            expiry=expiry,
                        )
                        newurl.save()
                        messages.success(request, "Your url is shortened Successfully. https://myurl.page/"+short)
                        return redirect(reverse('home:home')) # Saves the url in db & redirects to hom page.
                    else:
                        continue

            else:
                short = request.POST['short_char']
            # Check for generated char in user_urls table
            check = user_urls.objects.filter(short_char=short)
            if not check:
                newurl = user_urls(
                    user=usr,
                    title=title,
                    original_url=original,
                    short_char=short,
                    url_date=createdate,
                    expiry=expiry,
                )
                newurl.save()
                messages.success(request, "Your url is shortened Successfully. https://myurl.page/"+short)
                return redirect(reverse('home:home'))
            else:
                messages.error(request, "Custom URL You Entered is Already Exists")
                return redirect(reverse('home:home'))
        else:
            # generate randomly
            generated = False
            while not generated:
                short = randomgen()
                # Check for generated char in user_urls table
                check = user_urls.objects.filter(short_char=short)
                if not check:
                    newurl = public_urls(
                        original_url=original,
                        short_char=short,
                        url_date=createdate,
                        expiry=expiry,
                    )
                    newurl.save()
                    messages.success(request, "Your url is shortened Successfully. https://myurl.page/"+short)
                    return redirect(reverse('home:home'))
                else:
                    continue
    else:
        return redirect(reverse('home:home'))

# This function redirects short urls to original urls.
def redirection(request, query=None):
    if not query or query is None:
        return redirect(reverse('home:home'))
    else:
        try:
            # Checks in user_urls table
            check = user_urls.objects.get(short_char=query)
            check.visits = check.visits + 1
            check.save()
            url_to_redirect = check.original_url
            return redirect(url_to_redirect)
        except user_urls.DoesNotExist:
            try:
                # Checks in public_urls table
                check = public_urls.objects.get(short_char=query)
                check.visits = check.visits + 1
                check.save()
                url_to_redirect = check.original_url
                return redirect(url_to_redirect)
            except public_urls.DoesNotExist:
                #if query is not matched then redirects to home with error msg
                messages.info(request, "URL Expired or Does not exist.")
                return redirect(reverse('home:home'))

# Deletes the url
@login_required(login_url='/login/')
def deleteurl(request):
    if request.method == "POST":
        short = request.POST['delete']
        try:
            check = user_urls.objects.filter(short_char=short)
            check.delete()
            messages.success(request, "Deleted Successfully!")
            return redirect(reverse('dashboard:dashboard'))
        except user_urls.DoesNotExist:
            messages.error(request, "Something Has Gone Wrong")
            return redirect(home)
    else:
        return redirect(reverse('dashboard:dashboard'))
