from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('details', views.details, name='details'),
    path('questions', views.ques, name='ques'),
    path('social/singup',views.signup_redirect,name='signup_redirect'),
]
