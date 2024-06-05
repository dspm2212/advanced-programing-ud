from django.shortcuts import render

# Create your views here.

def home( request): 
    return render(request,'VirtualXperinces_app/home.html')

def login( request): 
    return render(request,'VirtualXperinces_app/login.html')

#def contact( request): 
    #return render(request,'virtualxperinces/contact.html') 

