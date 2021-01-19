from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home/home.html')
    
def about(request):
    return render(request, 'home/about.html')
    
def contactus(request):
    return render(request, 'home/contactus.html')
    
def features(request):
    return render(request, 'home/features.html')
    
def pricing(request):
    return render(request, 'home/pricing.html')