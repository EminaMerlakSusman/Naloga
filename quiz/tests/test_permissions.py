from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from rest_framework import status
from quiz.models import Question, Choice
from quiz.enums import UserGroups

class PermissionsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin_group = Group.objects.filter(name=UserGroups.ADMIN_USER.value).first()
        self.normal_group = Group.objects.filter(name=UserGroups.NORMAL_USER.value).first()

        self.admin_user = User.objects.create_user(username='admin', password='test')
        self.admin_user.groups.add(self.admin_group)

        self.normal_user = User.objects.create_user(username='user', password='test')
        self.normal_user.groups.add(self.normal_group)

        self.question_1 = Question.objects.create(question_text="How's it going?", owner=self.admin_user)
        self.choice_1 = Choice.objects.create(choice_text="Good, and you?", question=self.question_1)

        self.question_2 = Question.objects.create(question_text="Where does Santa live?", owner=self.normal_user)
        self.choice_2 = Choice.objects.create(choice_text="In Finland", question=self.question_2)

    def test_normal_user_question_permissions(self):
        self.client.login(username='user', password='test')
        with self.subTest("Should not be able to edit questions where I am not the owner"):
            response = self.client.patch(reverse('question-detail', kwargs={'pk': self.question_1.pk}), {'question_text': "How ya doing?"})
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        with self.subTest("Should be allowed to edit my own questions"):
            response = self.client.patch(reverse('question-detail', kwargs={'pk': self.question_2.pk}), {'question_text': "Does Santa exist?"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_normal_user_choice_permissions(self):
        self.client.login(username='user', password='test')
        with self.subTest("Should not be allowed to create choices for questions I don't own"):
            data = {'question': self.question_1.pk, 'choice_text': "Awesome"}
            response = self.client.post(reverse('choices'), data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.subTest("Should create choices where I am owner of question"):
            data = {'question': self.question_2.pk, 'choice_text': "On the North Pole"}
            response = self.client.post(reverse('choices'), data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        with self.subTest("Should not be able to edit choice where I am not the owner of question"):
            response = self.client.patch(reverse('choice-detail', kwargs={'pk': self.choice_1.pk}), {'choice_text': "Splendid!"})
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        with self.subTest("Should be able to edit choice for my own questions"):
            response = self.client.patch(reverse('choice-detail', kwargs={'pk': self.choice_2.pk}), {'choice_text': "Splendid!"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_admin_can_edit_other_users_questions(self):
        self.client.login(username='admin', password='test')
        response = self.client.patch(reverse('question-detail', kwargs={'pk': self.question_2.pk}), {'question_text': "How are you?"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
