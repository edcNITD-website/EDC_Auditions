from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('social/signup',views.signup_redirect,name='signup_redirect'),
    path('club-members',views.club_members,name='club_members'),
]