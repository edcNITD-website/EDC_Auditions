from django.shortcuts import render,redirect
from .models import Inductees


def home(request):
    return render(request,'home.html')

def signup_redirect(request):
    return redirect('home')

def club_members(request):
    user = request.user
    if user.is_authenticated:
        is_club_member = Inductees.objects.filter(user=user, is_club_member=True).exists()
        if is_club_member:
            students = Inductees.objects.filter(is_club_member=False)
            return render(request, 'admin.html',{'students':students})
    return redirect('home')