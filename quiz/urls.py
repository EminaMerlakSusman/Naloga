from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.SignupView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('questions/', views.QuestionsListCreateView.as_view(), name='questions'),
    path('questions/<int:pk>/', views.QuestionsRUDView.as_view(), name='question-detail'),
    path('choices/', views.ChoicesListCreateView.as_view(), name='choices'),
    path('choices/<int:pk>/', views.ChoicesRUDView.as_view(), name='choice-detail')
]