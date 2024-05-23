from django.shortcuts import render

# Create your views here.

def home( request): 
    return render(request,'virtualxperinces/home.html')

def login( request): 
    return render(request,'virtualxperinces/login.html')

def contact( request): 
    return render(request,'virtualxperinces/contact.html') 

