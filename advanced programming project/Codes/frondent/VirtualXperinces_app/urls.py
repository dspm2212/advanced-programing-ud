from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='xperiences_home'),
    path('login/', views.login, name="xperiences_login"),
]   