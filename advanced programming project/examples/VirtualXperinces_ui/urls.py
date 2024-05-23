from django.urls import path 
from. import views

urlpatterns = [

    path('',views.home, name='callender_home'), 
    path('contact/', views.contact, name="callender_contact"),
    path('login/', views.login, name="callender_login"),

]
  