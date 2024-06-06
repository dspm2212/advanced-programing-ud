from django.urls import path 
from. import views

urlpatterns = [
    path('',views.home, name='xperinces_home'), 
 #   path('contact/', views.contact, name="xperiences_contact"),
    path('login/', views.login, name="xperiences_login"),
    path('register/', views.register, name="xperiences_register"),
    path('dashboard/', views.dashboard, name="xperiences_dashboard"),
]   