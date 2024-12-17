from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Question, Choice
from .serializers import QuestionSerializer, ChoiceSerializer
from .permissions import IsQuestionOwnerOrAdmin, IsChoiceOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View


class SignupView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('login'))  # Redirect to the login page after signup
        return render(request, 'registration/signup.html', {'form': form})


class QuestionsListCreateView(ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated] # any user can view or create questions

    def perform_create(self, serializer):
        # set owner to logged-in user
        serializer.save(owner=self.request.user)


class QuestionsRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsQuestionOwnerOrAdmin]


class ChoicesListCreateView(ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated, IsChoiceOwnerOrAdmin]
    

class ChoicesRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated, IsChoiceOwnerOrAdmin]


