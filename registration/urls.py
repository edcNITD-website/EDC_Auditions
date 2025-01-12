from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('', views.Root.as_view(), name='root'),
    path("results", views.ResultsList.as_view(), name="results"),
    path("details", views.InducteesListCreateView.as_view(), name="details"),
    path("details/<int:pk>", views.InducteesDetailView.as_view(), name="details"),
    path("questions", views.QuestionListCreateView.as_view(), name="questions"),
    # path("questions/<int:pk>", views.QuestionDetailView.as_view(), name="questions"),
    path("comments", views.PostsListCreateView.as_view(), name="comments"),
    path("comments/<int:user_id>", views.PostsByUser.as_view(), name="comments"),
    # Authentication Paths
    path("signup", views.UserSignupView.as_view(), name="signup"),
    path("login", views.UserLoginView.as_view(), name="login"),
    #     path('social/signup',views.signup_redirect,name='signup_redirect'),
    #     path('login',views.handleLogin,name='handleLogin'),
    #     path('sign-up',views.handleSignUp,name='handleSignUp'),
    # Profile Paths
    path(
        "club-members", views.ClubMembersListCreateView.as_view(), name="club_members"
    ),
    #     path('club-members/search/<str:category>/<str:search_term>',views.search,name='search'),
    #     path('club-members/filter/<int:type>',views.filter,name='filter'),
    #     path('club-members/inductees/<int:id>',views.student_profile,name='student_profile'),
    #     path('like/<int:id>',views.like,name='like_student'),
    #     path('mark/<int:id>/<int:type>',views.mark,name="mark"),
    # CSV Paths
    path("export/csv", views.export_to_csv, name="export_to_csv"),
    #     path('StudentsCSV', views.StudentsCSV, name="StudentsCSV"),
    # path("WebCSV", views.WEBCSV, name="WEBCSV"),
    #     path('EventCSV', views.eventCSV, name="EventCSV"),
    #     path('ContentCSV', views.contentCSV, name="ContentCSV"),
    #     path('TechCSV', views.videoCSV, name="TechCSV"),
    #     path('GraphicCSV', views.GdCSV, name="GraphicCSV"),
    #     path('MaleCSV', views.MaleCSV, name="MaleCSV"),
    #     path('FemaleCSV', views.FemaleCSV, name="FemaleCSV"),
    #     path('RecentCSV', views.getPosts, name="RecentCSV"),
    # JWT endpoints
    path('auth/token', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # Response Paths
    path("responses", views.ResponseListCreateView.as_view(), name="responses"),
    path("responses/<int:user_id>", views.ResponseByUser.as_view(), name="responses"),
]
