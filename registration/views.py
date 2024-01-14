from django.shortcuts import render,redirect, get_object_or_404
from .models import Inductees,Question, Response, Posts, Result
from . forms import BasicDetailsForm, QuestionsForm, PostsForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import ast, csv

def home(request):
    if request.user.is_authenticated:
        user = request.user
        if Inductees.objects.filter(user=user).exists():
            student = get_object_or_404(Inductees, user = user)
            if student.is_club_member:
                return render(request,'home.html',{'message':'Welcome Admin!!','admin':True})
        return render(request,'home.html',{'message':'Checkout your profile'})
    return render(request,'home.html')

def signup_redirect(request):
    return render(request,'home.html')

def results(request):
    if Result.objects.all().exists():
        maxround = Result.objects.all().order_by('-round')[0].round
    else:
        maxround = 0
    results = Result.objects.filter(round=maxround)
    return render(request,'results.html',{'winners':results,'round':maxround})

def club_members(request):
    user = request.user
    if user.is_authenticated:
        is_club_member = Inductees.objects.filter(user=user, is_club_member=True).exists()
        if is_club_member:
            students = Inductees.objects.filter(is_club_member=False).order_by('-round')
            return render(request, 'admin.html',{'students':students,'admin':True})
        else:
            return render(request,'home.html',{'message':'You are not an admin :( '})       
    return render(request,'home.html',{'message':'Please login to continue'})

def search(request,search_term="",category=""):
    user = request.user
    students = []
    if user.is_authenticated:
        is_club_member = Inductees.objects.filter(user=user, is_club_member=True).exists()
        if is_club_member:
            if request.method == "GET":
                if category == "name":
                    if search_term == "":
                        students = Inductees.objects.filter(is_club_member=False)
                    else:
                        students = Inductees.objects.filter(is_club_member=False,full_name__icontains=search_term).order_by('-round')
                elif category == "roll":
                    if search_term == "":
                        students = Inductees.objects.filter(is_club_member=False)
                    else:
                        students = Inductees.objects.filter(is_club_member=False,rollnumber__icontains=search_term).order_by('-round')
                elif category == "branch":
                    if search_term == "":
                        students = Inductees.objects.filter(is_club_member=False)
                    else:
                        students = Inductees.objects.filter(is_club_member=False,department__icontains=search_term).order_by('-round')
            return render(request, 'admin.html',{'students':students,'message':f'Search results for {search_term}','admin':True})
    return redirect('home')

def student_profile(request,id):
    user = request.user
    if user.is_authenticated:
        is_club_member = Inductees.objects.filter(user=user, is_club_member=True).exists()
        if is_club_member:
            student = Inductees.objects.get(id=id)
            if student.domains != "":
                student.domains = ast.literal_eval(student.domains)
            else:
                student.domains = []
            comments = Posts.objects.filter(user=student)
            likes = student.total_likes()
            answers = Response.objects.filter(student=student)
            form = PostsForm(request.POST)
            allow = Inductees.objects.get(user = user).year
            liked = False
            if student.like.filter(id=user.id).exists():
                liked = True
            if form.is_valid():
                post = Posts(
                    user = student,
                    comment = form.cleaned_data['comment'],
                    round = form.cleaned_data['round'],
                    by = Inductees.objects.get(user = user).full_name,
                    year = Inductees.objects.get(user = user).year,
                )
                post.save()
                return redirect('student_profile',id=id)
            return render(request,'student_profile.html',{'student':student,'comments2':comments.filter(year = 2).order_by('-round'),'comments3':comments.filter(year=3).order_by('-round'),'comments4':comments.filter(year=4).order_by('-round'), 'form':form, 'answers':answers, 'allow':allow,'likes':likes,'liked':liked,'admin':True})
        return redirect('home') 
    return redirect('home')

def details(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = BasicDetailsForm(request.POST)
            if form.is_valid():
                if Inductees.objects.filter(user=request.user).exists() :
                    student = get_object_or_404(Inductees, user = request.user)
                    student.full_name = form.cleaned_data['name']
                    student.gender = form.cleaned_data['gender']
                    student.registration_no = form.cleaned_data['registration_no']
                    student.rollnumber = form.cleaned_data['roll_no']
                    student.department = form.cleaned_data['branch']
                    student.place = form.cleaned_data['place']
                    student.phone_number = form.cleaned_data['Mobile_Number']
                    student.year = form.cleaned_data['year']
                    student.domains = form.cleaned_data['domains']
                    student.save()
                    return redirect('ques')
                else:
                    return redirect('home')
        else:
            if Inductees.objects.filter(user=request.user).exists():
                student = get_object_or_404(Inductees, user = request.user)
                choices = student.domains
                if choices != "":
                    options = ast.literal_eval(choices)
                else:
                    options = []
                form = BasicDetailsForm(initial={
                'name': student.full_name,
                'gender': student.gender,
                'registration_no': student.registration_no,
                'roll_no': student.rollnumber,
                'branch': student.department,
                'place': student.place,
                'Mobile_Number': student.phone_number,
                'year': student.year,
                'domains': options,
                })
            else:
                form = BasicDetailsForm()
        return render(request, 'detailsform.html', {'form': form})
    else:
        return render(request,'home.html',{'message':'Please login to continue'})

def ques(request):
    if request.user.is_authenticated:
        if Inductees.objects.filter(user=request.user).exists():
            student = get_object_or_404(Inductees, user = request.user)
            if student.registration_no=="":
                return redirect('details')
            questions = Question.objects.all()
            if request.method == 'POST':        
                form = QuestionsForm(request.POST)
                if form.is_valid():               
                    if Response.objects.filter(student=student).exists():
                        for q in questions:
                            response = get_object_or_404(Response, student = student, question = q)
                            response.answer = form.cleaned_data[f'{q.id}']
                            response.save()
                    else:
                        for q in questions:
                            response = Response(
                            student = student,
                            question = q,
                            answer = form.cleaned_data[f'{q.id}'] 
                            )
                            response.save()
                    return render(request, 'home.html', {'message':'Your response has been recorded'})
                else:
                    return render(request, 'questions.html', {'form' : form})
            else:
                if Response.objects.filter(student=student).exists():
                    responses = get_object_or_404(Inductees, user = request.user)
                    formData = {}
                    for q in questions:
                        formData[f'{q.id}'] = get_object_or_404(Response, student= student, question = q).answer
                    form = QuestionsForm(initial= formData)
                else:
                    form = QuestionsForm()
                return render(request, 'questions.html', {'form' : form})
        else:
            return redirect('details')
    else:
        return render(request,'home.html',{'message':'Please login to continue'})

def like(request,id):
    user = request.user
    if user.is_authenticated:
        is_club_member = Inductees.objects.filter(user=user, is_club_member=True).exists()
        if is_club_member:
            student = Inductees.objects.get(id=id)
            liked = False
            if student.like.filter(id=user.id).exists():
                student.like.remove(user)
                liked = False
            else:
                liked = True
                student.like.add(user)
            return HttpResponseRedirect(reverse('student_profile', args=[str(id)]))
    return redirect('home')

def filter(request,type):
    user = request.user
    if user.is_authenticated:
        is_club_member = Inductees.objects.filter(user=user, is_club_member=True).exists()
        students = []
        if is_club_member:
            if request.method=='GET':
                students = Inductees.objects.filter(is_club_member=False,color = type).order_by('-round')
            return render(request, 'admin.html',{'students':students})
        else:
            return redirect('home')
    else:
        return redirect('home')

def mark(request,id,type):
    user = request.user
    if user.is_authenticated:
        is_club_member = Inductees.objects.filter(user=user, is_club_member=True).exists()
        if is_club_member:
            if request.method=='POST':
                student = get_object_or_404(Inductees, id = id)
                student.color = type
                student.save()
            return HttpResponseRedirect(reverse('student_profile', args=[str(id)]))
        else:
            return redirect('home')
    else:
        return redirect('home')
    

def StudentsCSV(request):
    if request.user.username == 'admin':
        students = Inductees.objects.filter(is_club_member=False).all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="students.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Roll Number', 'Department', 'Year', 'Domains', 'Round', 'Color'])
        for student in students:
            writer.writerow([student.full_name, student.rollnumber, student.department, student.year, student.domains, student.round, student.color])
        return response

def WEBCSV(request):
    if request.user.username == 'admin':
        students = Inductees.objects.filter(is_club_member=False,domains__icontains='WEB/APP DEVELOPEMENT').all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="web.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Roll Number', 'Department', 'Year', 'Domains', 'Round', 'Color'])
        for student in students:
            writer.writerow([student.full_name, student.rollnumber, student.department, student.year, student.domains, student.round, student.color])
        return response
    
def GdCSV(request):
    if request.user.username == 'admin':
        students = Inductees.objects.filter(is_club_member=False,domains__icontains='GRAPHIC DESIGNING').all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="gd.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Roll Number', 'Department', 'Year', 'Domains', 'Round', 'Color'])
        for student in students:
            writer.writerow([student.full_name, student.rollnumber, student.department, student.year, student.domains, student.round, student.color])
        return response
    
def contentCSV(request):
    if request.user.username == 'admin':
        students = Inductees.objects.filter(is_club_member=False,domains__icontains='CONTENT WRITING').all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="content.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Roll Number', 'Department', 'Year', 'Domains', 'Round', 'Color'])
        for student in students:
            writer.writerow([student.full_name, student.rollnumber, student.department, student.year, student.domains, student.round, student.color])
        return response
    
def eventCSV(request):
    if request.user.username == 'admin':
        students = Inductees.objects.filter(is_club_member=False,domains__icontains='EVENT MANAGEMENT').all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="event.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Roll Number', 'Department', 'Year', 'Domains', 'Round', 'Color'])
        for student in students:
            writer.writerow([student.full_name, student.rollnumber, student.department, student.year, student.domains, student.round, student.color])
        return response
        
def videoCSV(request):
    if request.user.username == 'admin':
        students = Inductees.objects.filter(is_club_member=False,domains__icontains='VIDEO EDITING').all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="video.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Roll Number', 'Department', 'Year', 'Domains', 'Round', 'Color'])
        for student in students:
            writer.writerow([student.full_name, student.rollnumber, student.department, student.year, student.domains, student.round, student.color])
        return response