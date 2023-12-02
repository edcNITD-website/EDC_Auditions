from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('social/singup',views.signup_redirect,name='signup_redirect'),
]