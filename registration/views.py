from django.shortcuts import render, redirect, get_object_or_404
from .models import Inductees, Question, Response, Posts, Result
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import BasicDetailsForm, QuestionsForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
import ast, csv
from django.db.models import Q
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.decorators import api_view, permission_classes
from .serializers import (
    QuestionSerializer,
    ResultSerializer,
    InducteesSerializer,
    SignupSerializer,
    LoginSerializer,
    PostsSerializer,
    ResponseSerializer,
    CustomTokenObtainPairSerializer,
)
from rest_framework import generics, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

# conflict from Response model
from rest_framework.response import Response as RestResponse

from rest_framework.permissions import BasePermission, IsAuthenticated


class IsClubMember(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.inductees.is_club_member
        print("hello")
        return request.data.is_authenticated
 
        return request.user.inductees.is_club_member


# TODO: use viewsets in future for restful api


class UserSignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer


class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            refresh = RefreshToken.for_user(user)
            refresh["is_club_member"] = user.inductees.is_club_member
            refresh["student_id"] = user.inductees.id
            refresh["username"] = user.username
            return RestResponse(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "message": "Logged in successfully",
                },
                status=status.HTTP_200_OK,
            )

        return RestResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InducteesListCreateView(generics.ListCreateAPIView):
    queryset = Inductees.objects.all().filter(is_club_member=False)
    serializer_class = InducteesSerializer
    authenication_classes = [JWTAuthentication]
    permission_classes = [IsClubMember]

    # def get_permissions(self):
    #     return [IsClubMember()]
        # if self.request.method == 'GET':
        #     # Allow authenticated users for GET requests
        #     return [IsAuthenticated()]
        # elif self.request.method == 'POST':
        #     # Allow only club members for POST requests
        #     return [IsAuthenticated(), IsClubMember()]
        # return super().get_permissions()


class InducteesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inductees.objects.all().filter(is_club_member=False)
    serializer_class = InducteesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsClubMember]
    # permission_classes = [IsAdminUser, IsAuthenticated]


class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        elif self.request.method == "POST":
            return [IsClubMember()] 
        return super().get_permissions()

class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [JWTAuthentication]

    # permission_classes = [IsAuthenticated]


class ResultListView(generics.ListAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    # permission_classes = [IsAuthenticated, IsAuthenticated]


class ClubMembersListCreateView(generics.ListCreateAPIView):
    queryset = Inductees.objects.all().filter(is_club_member=True)
    serializer_class = InducteesSerializer
    # permission_classes = [IsAdminUser, IsAuthenticated]


class PostsListCreateView(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsClubMember]
    # permission_classes = [IsAuthenticated]


class PostsByUser(generics.ListAPIView):
    serializer_class = PostsSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Posts.objects.filter(user=user_id)

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClubMember]


class ResponseListCreateView(generics.ListCreateAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClubMember]
    # permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     try:
    #         student = self.request.user.inductees
    #         serializer.save(student=student)
    #     except Exception as e:
    #        print("User does not have an inductee profile", e)

    # def perform_create(self, serializer):
    #     if hasattr(self.request.user, 'inductees'):
    #         student = self.request.user.inductees
    #         response = serializer.save(student=student)
    #         print(f"Response saved: {response}")  # Debug log
    #     else:
    #         raise serializers.ValidationError({"error": "User does not have an inductee profile"})


# class ResponseDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Response.objects.all()
#     serializer_class = ResponseSerializer
#     # permission_classes = [IsAuthenticated, IsAuthenticated]


class ResponseByUser(generics.ListAPIView):
    serializer_class = ResponseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClubMember]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Response.objects.filter(student=user_id)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ResultsList(generics.ListAPIView):
    queryset = Inductees.objects.all().filter(color = 3)
    serializer_class = InducteesSerializer


@api_view(["GET"])
# @permission_classes([IsAdminUser, IsAuthenticated])
def export_to_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="inductees.csv"'

    writer = csv.writer(response)

    writer.writerow(
        [
            "Name",
            "Roll Number",
            "Department",
            "Year",
            "Domains",
            "Round",
            "Color",
            "Phone Number",
            "Gender",
            "Domains",
        ]
    )

    gender = request.query_params.get("gender")
    domain = request.query_params.get("domain")

    inductees = Inductees.objects.all()

    if gender:
        inductees = inductees.filter(gender=gender)

    if domain:
        inductees = inductees.filter(domains__icontains=domain)

    for inductee in inductees:
        writer.writerow(
            [
                inductee.full_name,
                inductee.rollnumber,
                inductee.department,
                inductee.year,
                inductee.domains,
                inductee.round,
                inductee.color,
                inductee.phone_number,
                inductee.gender,
                inductee.domains,
            ]
        )

    return response


def home(request):
    if request.user.is_authenticated:
        user = request.user
        if Inductees.objects.filter(user=user).exists():
            student = get_object_or_404(Inductees, user=user)
            if student.is_club_member:
                return render(
                    request, "home.html", {"message": "Welcome Admin!!", "admin": True}
                )
        return render(request, "home.html", {"message": "Checkout your profile"})
    return render(request, "home.html")


def signup_redirect(request):
    return render(request, "home.html")


@api_view(["GET"])
# @permission_classes([IsAuthenticated, IsAuthenticated])
def results(request):
    # if Result.objects.all().exists():
    #     maxround = Result.objects.all().order_by('-round')[0].round
    # else:
    #     maxround = 0
    # results = Result.objects.filter(round=maxround)
    results = Result.objects.all()
    serializer = ResultSerializer(results, many=True)
    # if request.user.is_authenticated:
    #     student = get_object_or_404(Inductees, user = request.user)
    #     admin = student.is_club_member
    # else:
    #     admin = False
    return Response(serializer.data)


@api_view(["GET"])
# @permission_classes([IsAuthenticated, IsAuthenticated])
def club_members(request):
    user = request.user
    # if user.is_authenticated:
    if True:
        # is_club_member = Inductees.objects.filter(user=user, is_club_member=True).exists()
        # if is_club_member:
        if True:
            # students = list(Inductees.objects.filter(is_club_member=False).order_by('-round').values())
            students = Inductees.objects.filter(is_club_member=False).order_by("-round")
            # return JsonResponse({"students": students, "admin": True})
            serializer = ResultSerializer(students, many=True)
            return Response(serializer.data)
        else:
            return render(request, "home.html", {"message": "You are not an admin :( "})
    # return render(request,'home.html',{'message':'Please login to continue'})


def search(request, search_term="", category=""):
    user = request.user
    students = []
    if user.is_authenticated:
        is_club_member = Inductees.objects.filter(
            user=user, is_club_member=True
        ).exists()
        if is_club_member:
            if request.method == "GET":
                if category == "name":
                    if search_term == "":
                        students = Inductees.objects.filter(is_club_member=False)
                    else:
                        students = Inductees.objects.filter(
                            is_club_member=False, full_name__icontains=search_term
                        ).order_by("-round")
                elif category == "roll":
                    if search_term == "":
                        students = Inductees.objects.filter(is_club_member=False)
                    else:
                        students = Inductees.objects.filter(
                            is_club_member=False, rollnumber__icontains=search_term
                        ).order_by("-round")
                elif category == "branch":
                    if search_term == "":
                        students = Inductees.objects.filter(is_club_member=False)
                    else:
                        students = Inductees.objects.filter(
                            is_club_member=False, department__icontains=search_term
                        ).order_by("-round")
            serializer = ResultSerializer(students, many=True)
            # return JsonResponse({"students": list(students.values()), "admin": True})
            return Response(serializer.data)
    return redirect("home")


def student_profile(request, id):
    user = request.user
    if user.is_authenticated:
        is_club_member = Inductees.objects.filter(
            user=user, is_club_member=True
        ).exists()
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
            allow = Inductees.objects.get(user=user).year
            liked = False
            if student.like.filter(id=user.id).exists():
                liked = True
            if form.is_valid():
                post = Posts(
                    user=student,
                    comment=form.cleaned_data["comment"],
                    round=form.cleaned_data["round"],
                    by=Inductees.objects.get(user=user).full_name,
                    year=Inductees.objects.get(user=user).year,
                )
                post.save()
                return redirect("student_profile", id=id)
            return render(
                request,
                "student_profile.html",
                {
                    "student": student,
                    "comments2": comments.filter(year=2).order_by("-round"),
                    "comments3": comments.filter(year=3).order_by("-round"),
                    "comments4": comments.filter(year=4).order_by("-round"),
                    "form": form,
                    "answers": answers,
                    "allow": allow,
                    "likes": likes,
                    "liked": liked,
                    "admin": True,
                },
            )
        return redirect("home")
    return redirect("home")


def details(request):
    if request.user.is_authenticated:
        student = get_object_or_404(Inductees, user=request.user)
        admin = student.is_club_member
        if request.method == "POST":
            form = BasicDetailsForm(request.POST)
            if form.is_valid():
                if Inductees.objects.filter(user=request.user).exists():
                    student = get_object_or_404(Inductees, user=request.user)
                    student.full_name = form.cleaned_data["name"]
                    student.gender = form.cleaned_data["gender"]
                    student.registration_no = form.cleaned_data["registration_no"]
                    student.rollnumber = form.cleaned_data["roll_no"]
                    student.department = form.cleaned_data["branch"]
                    student.place = form.cleaned_data["place"]
                    student.phone_number = form.cleaned_data["Mobile_Number"]
                    student.year = form.cleaned_data["year"]
                    student.domains = form.cleaned_data["domains"]
                    student.save()
                    return redirect("ques")
                else:
                    return redirect("home")
        else:
            if Inductees.objects.filter(user=request.user).exists():
                student = get_object_or_404(Inductees, user=request.user)
                choices = student.domains
                if choices != "":
                    options = ast.literal_eval(choices)
                else:
                    options = []
                form = BasicDetailsForm(
                    initial={
                        "name": student.full_name,
                        "gender": student.gender,
                        "registration_no": student.registration_no,
                        "roll_no": student.rollnumber,
                        "branch": student.department,
                        "place": student.place,
                        "Mobile_Number": student.phone_number,
                        "year": student.year,
                        "domains": options,
                    }
                )
            else:
                form = BasicDetailsForm()

        return render(request, "detailsform.html", {"form": form, "admin": admin})
    else:
        return render(request, "home.html", {"message": "Please login to continue"})


@api_view(["GET"])
def ques(request):
    return Response(QuestionSerializer(Question.objects.all(), many=True).data)
    if request.user.is_authenticated:
        student = get_object_or_404(Inductees, user=request.user)
        admin = student.is_club_member
        if Inductees.objects.filter(user=request.user).exists():
            student = get_object_or_404(Inductees, user=request.user)
            if student.registration_no == "":
                return redirect("details")
            questions = Question.objects.all()
            if request.method == "POST":
                form = QuestionsForm(request.POST)
                if form.is_valid():
                    if Response.objects.filter(student=student).exists():
                        for q in questions:
                            response = get_object_or_404(
                                Response, student=student, question=q
                            )
                            response.answer = form.cleaned_data[f"{q.id}"]
                            response.save()
                    else:
                        for q in questions:
                            response = Response(
                                student=student,
                                question=q,
                                answer=form.cleaned_data[f"{q.id}"],
                            )
                            response.save()
                    return render(
                        request,
                        "home.html",
                        {"message": "Your response has been recorded"},
                    )
                else:
                    return render(request, "questions.html", {"form": form})
            else:
                if Response.objects.filter(student=student).exists():
                    responses = get_object_or_404(Inductees, user=request.user)
                    formData = {}
                    for q in questions:
                        formData[f"{q.id}"] = get_object_or_404(
                            Response, student=student, question=q
                        ).answer
                    form = QuestionsForm(initial=formData)
                else:
                    form = QuestionsForm()
                return render(request, "questions.html", {"form": form, "admin": admin})
        else:
            return redirect("details")
    else:
        return render(request, "home.html", {"message": "Please login to continue"})


def like(request, id):
    user = request.user
    if user.is_authenticated:
        is_club_member = Inductees.objects.filter(
            user=user, is_club_member=True
        ).exists()
        if is_club_member:
            student = Inductees.objects.get(id=id)
            liked = False
            if student.like.filter(id=user.id).exists():
                student.like.remove(user)
                liked = False
            else:
                liked = True
                student.like.add(user)
            return HttpResponseRedirect(reverse("student_profile", args=[str(id)]))
    return redirect("home")


def filter(request, type):
    user = request.user
    if user.is_authenticated:
        is_club_member = Inductees.objects.filter(
            user=user, is_club_member=True
        ).exists()
        students = []
        if is_club_member:
            if request.method == "GET":
                students = Inductees.objects.filter(
                    is_club_member=False, color=type
                ).order_by("-round")
            return JsonResponse({"students": list(students.values()), "admin": True})
        else:
            return redirect("home")
    else:
        return redirect("home")


def mark(request, id, type):
    user = request.user
    if user.is_authenticated:
        is_club_member = Inductees.objects.filter(
            user=user, is_club_member=True
        ).exists()
        if is_club_member:
            if request.method == "POST":
                student = get_object_or_404(Inductees, id=id)
                student.color = type
                student.save()
            return HttpResponseRedirect(reverse("student_profile", args=[str(id)]))
        else:
            return redirect("home")
    else:
        return redirect("home")


def StudentsCSV(request):
    if request.user.username == "admin":
        students = Inductees.objects.filter(is_club_member=False).all()
        students.order_by("-round")
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="students.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "Name",
                "Roll Number",
                "Department",
                "Year",
                "Domains",
                "Round",
                "Color",
                "Phone Number",
                "Gender",
            ]
        )
        for student in students:
            writer.writerow(
                [
                    student.full_name,
                    student.rollnumber,
                    student.department,
                    student.year,
                    student.domains,
                    student.round,
                    student.color,
                    student.phone_number,
                    student.gender,
                ]
            )
        return response
    else:
        return redirect("home")


@api_view(["GET"])
def WEBCSV(request):
    # if request.user.username == 'admin':
    if True:
        students = Inductees.objects.filter(
            is_club_member=False, domains__icontains="WEB/APP DEVELOPEMENT"
        ).all()
        students.order_by("-round")
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="web.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "Name",
                "Roll Number",
                "Department",
                "Year",
                "Domains",
                "Round",
                "Color",
                "Phone Number",
                "Gender",
            ]
        )
        for student in students:
            writer.writerow(
                [
                    student.full_name,
                    student.rollnumber,
                    student.department,
                    student.year,
                    student.domains,
                    student.round,
                    student.color,
                    student.phone_number,
                    student.gender,
                ]
            )
        return response
    # else:
    #     return redirect('home')


def GdCSV(request):
    if request.user.username == "admin":
        students = Inductees.objects.filter(
            is_club_member=False, domains__icontains="GRAPHIC DESIGNING"
        ).all()
        students.order_by("-round")
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="gd.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "Name",
                "Roll Number",
                "Department",
                "Year",
                "Domains",
                "Round",
                "Color",
                "Phone Number",
                "Gender",
            ]
        )
        for student in students:
            writer.writerow(
                [
                    student.full_name,
                    student.rollnumber,
                    student.department,
                    student.year,
                    student.domains,
                    student.round,
                    student.color,
                    student.phone_number,
                    student.gender,
                ]
            )
        return response
    else:
        return redirect("home")


def contentCSV(request):
    if request.user.username == "admin":
        students = Inductees.objects.filter(
            is_club_member=False, domains__icontains="CONTENT WRITING"
        ).all()
        students.order_by("-round")
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="content.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "Name",
                "Roll Number",
                "Department",
                "Year",
                "Domains",
                "Round",
                "Color",
                "Phone Number",
                "Gender",
            ]
        )
        for student in students:
            writer.writerow(
                [
                    student.full_name,
                    student.rollnumber,
                    student.department,
                    student.year,
                    student.domains,
                    student.round,
                    student.color,
                    student.phone_number,
                    student.gender,
                ]
            )
        return response
    else:
        return redirect("home")


def eventCSV(request):
    if request.user.username == "admin":
        students = Inductees.objects.filter(
            is_club_member=False, domains__icontains="EVENT MANAGEMENT"
        ).all()
        students.order_by("-round")
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="event.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "Name",
                "Roll Number",
                "Department",
                "Year",
                "Domains",
                "Round",
                "Color",
                "Phone Number",
                "Gender",
            ]
        )
        for student in students:
            writer.writerow(
                [
                    student.full_name,
                    student.rollnumber,
                    student.department,
                    student.year,
                    student.domains,
                    student.round,
                    student.color,
                    student.phone_number,
                    student.gender,
                ]
            )
        return response
    else:
        return redirect("home")


def videoCSV(request):
    if request.user.username == "admin":
        students = Inductees.objects.filter(
            is_club_member=False, domains__icontains="VIDEO EDITING"
        ).all()
        students.order_by("-round")
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="video.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "Name",
                "Roll Number",
                "Department",
                "Year",
                "Domains",
                "Round",
                "Color",
                "Phone Number",
                "Gender",
            ]
        )
        for student in students:
            writer.writerow(
                [
                    student.full_name,
                    student.rollnumber,
                    student.department,
                    student.year,
                    student.domains,
                    student.round,
                    student.color,
                    student.phone_number,
                    student.gender,
                ]
            )
        return response
    else:
        return redirect("home")


def handleLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_obj = User.objects.filter(email=email).first()
        if user_obj is None:
            messages.success(request, "Please create an account first")
            return redirect("/login")
        user = authenticate(username=email, password=password)
        if user is None:
            messages.success(request, "Wrong password or email address")
            return redirect("/login")
        login(request, user)
        messages.success(request, "Logged in successfully")
        return redirect("/details")
    else:
        if request.user.is_authenticated:
            return redirect("/details")
        return render(request, "login.html")


def handleSignUp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        try:
            if User.objects.filter(email=email).first():
                messages.success(request, "Email already exists. Login in to continue")
                return redirect("/login")
            if str(password1) != str(password2):
                messages.success(request, "Passwords do not match")
                return redirect("/sign-up")
            user = User.objects.create_user(email, email, password1)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            full_name = first_name + " " + last_name
            profile_picture = "https://ui-avatars.com/api/?name=" + full_name.replace(
                " ", "+"
            )
            inductee = Inductees(
                user=user, full_name=full_name, profile_picture=profile_picture
            )
            inductee.save()
            messages.success(request, "Account created successfully")
            return redirect("/login")
        except Exception as e:
            messages.success(request, "Something went wrong")
            return redirect("/")
    else:
        if request.user.is_authenticated:
            return redirect("/details")
        return render(request, "sign-up.html")


def MaleCSV(request):
    if request.user.username == "admin":
        students = Inductees.objects.filter(
            Q(gender="M") | Q(gender=""), is_club_member=False
        ).all()
        students = students.order_by("-round", "-gender")
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="malestudents.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "Name",
                "Roll Number",
                "Department",
                "Year",
                "Domains",
                "Round",
                "Color",
                "Phone Number",
                "Gender",
            ]
        )
        for student in students:
            writer.writerow(
                [
                    student.full_name,
                    student.rollnumber,
                    student.department,
                    student.year,
                    student.domains,
                    student.round,
                    student.color,
                    student.phone_number,
                    student.gender,
                ]
            )
        return response
    else:
        return redirect("home")


def FemaleCSV(request):
    if request.user.username == "admin":
        students = Inductees.objects.filter(
            is_club_member=False,
            gender="F",
        ).all()
        students.order_by("-round")
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="femalestudents.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "Name",
                "Roll Number",
                "Department",
                "Year",
                "Domains",
                "Round",
                "Color",
                "Phone Number",
                "Gender",
            ]
        )
        for student in students:
            writer.writerow(
                [
                    student.full_name,
                    student.rollnumber,
                    student.department,
                    student.year,
                    student.domains,
                    student.round,
                    student.color,
                    student.phone_number,
                    student.gender,
                ]
            )
        return response
    else:
        return redirect("home")


def getPosts(request):
    # get posts from database in -date order and separate out max date people and search them on inductees and return them
    if request.user.username == "admin":
        posts = Posts.objects.all().order_by("-date")
        maxdate = posts[0].date
        maxdateposts = posts.filter(date=maxdate)
        students = []
        for post in maxdateposts:
            students.append(post.user)
        # remove repetitions
        students = list(dict.fromkeys(students))
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="recentstudents.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "Name",
                "Roll Number",
                "Department",
                "Year",
                "Domains",
                "Round",
                "Color",
                "Phone Number",
                "Gender",
            ]
        )
        for student in students:
            writer.writerow(
                [
                    student.full_name,
                    student.rollnumber,
                    student.department,
                    student.year,
                    student.domains,
                    student.round,
                    student.color,
                    student.phone_number,
                    student.gender,
                ]
            )
        return response
    else:
        return redirect("home")
