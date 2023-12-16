from django.shortcuts import render, redirect, get_object_or_404
from . forms import BasicDetailsForm, QuestionsForm
from . models import Student,Question, User, Response
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request,'home.html')

def signup_redirect(request):
    return render(request,'home.html')

@login_required
def details(request):
    if request.method == 'POST':
        form = BasicDetailsForm(request.POST)
        if form.is_valid():
            if Student.objects.filter(user=request.user).exists() :
                student = get_object_or_404(Student, user = request.user)
                student.name = form.cleaned_data['name']
                student.email = form.cleaned_data['email']
                student.gender = form.cleaned_data['gender']
                student.registration_no = form.cleaned_data['registration_no']
                student.roll_no = form.cleaned_data['roll_no']
                student.branch = form.cleaned_data['branch']
                student.place = form.cleaned_data['place']
                student.save()
                return redirect('/questions')
            else :
                student = Student(
                    user = request.user,
                    name = form.cleaned_data['name'],
                    email = form.cleaned_data['email'],
                    gender = form.cleaned_data['gender'],
                    registration_no = form.cleaned_data['registration_no'],
                    roll_no = form.cleaned_data['roll_no'],
                    branch = form.cleaned_data['branch'],
                    place = form.cleaned_data['place']
                )
                student.save()
                return redirect('/questions')
    else:
        if Student.objects.filter(user=request.user).exists():
            student = get_object_or_404(Student, user = request.user)
            form = BasicDetailsForm(initial={
            'name': student.name,
            'email': student.email,
            'gender': student.gender,
            'registration_no': student.registration_no,
            'roll_no': student.roll_no,
            'branch': student.branch,
            'place': student.place
            })
        else:
            form = BasicDetailsForm()
    return render(request, 'detailsform.html', {'form': form})

@login_required
def ques(request):
    if Student.objects.filter(user=request.user).exists():
        student = get_object_or_404(Student, user = request.user)
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
                return redirect('/')
            else:
                return render(request, 'questions.html', {'form' : form})
       
        else:
            if Response.objects.filter(student=student).exists():
                responses = get_object_or_404(Student, user = request.user)
                formData = {}
                for q in questions:
                    formData[f'{q.id}'] = get_object_or_404(Response, student= student, question = q).answer
                form = QuestionsForm(initial= formData)
            else:
                form = QuestionsForm()
            return render(request, 'questions.html', {'form' : form})
    else:
        return redirect('/details')