from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User, Group
from quiz.models import Question, Choice
from django.urls import reverse
from quiz.enums import UserGroups


class QuestionViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        # create admin user and login
        self.admin_group = Group.objects.filter(name=UserGroups.ADMIN_USER.value).first()
        self.admin_user = User.objects.create_user(username='admin', password='test')
        self.admin_user.groups.add(self.admin_group)
        self.client.login(username='admin', password='test')

        self.question_1 = Question.objects.create(question_text="How's it going?", owner=self.admin_user)
        self.choice_1 = Choice.objects.create(question=self.question_1, choice_text="Good")
    
    def test_list_questions(self):
        response = self.client.get(reverse('questions'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        question_data = {
            'id': 1, 
            'question_text': "How's it going?",
            'choices': [
                {'id': 1, 
                'choice_text': 'Good',
                'votes': 0,
                'question': 1}
                ],
            'owner': self.admin_user.pk
            }
        self.assertEqual(response.data[0], question_data)
        self.assertEqual(len(response.data), 1)

    def test_create_question(self):
        data = {'question_text': "Does Santa exist?"}
        response = self.client.post(reverse('questions'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)
    
    def test_update_question(self):
        data = {'question_text': "How ya doing?"}
        response = self.client.put(reverse('question-detail', kwargs={'pk': self.question_1.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        question_data = {'id': 1, 
                'question_text': 'How ya doing?', 
                'choices': [
                    {'id': 1, 
                    'choice_text': 'Good',
                    'votes': 0,
                    'question': 1}
                ],
                'owner': self.admin_user.pk
                }
        self.assertEqual(response.data, question_data)

    def test_retrieve_question(self):
        response = self.client.get(reverse('question-detail', kwargs={'pk': self.question_1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.question_1.pk)
    
    def test_delete_question(self):
        response = self.client.delete(reverse('question-detail', kwargs={'pk': self.question_1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.count(), 0)

    

class ChoiceViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # create admin user and login
        self.admin_group = Group.objects.filter(name=UserGroups.ADMIN_USER.value).first()
        self.admin_user = User.objects.create_user(username='admin', password='test')
        self.admin_user.groups.add(self.admin_group)
        self.client.login(username='admin', password='test')

        self.question_1 = Question.objects.create(question_text="What is the meaning of life?", owner=self.admin_user)
        self.choice_1 = Choice.objects.create(question=self.question_1, choice_text="Ležanje na plaži")

    def test_list_choices(self):
        response = self.client.get(reverse('choices'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        choice_data = {
            'id': self.choice_1.pk, 
            'choice_text': 'Ležanje na plaži', 
            'votes': 0, 
            'question': 1
            }
             
        self.assertEqual(response.data[0], choice_data)
        self.assertEqual(len(response.data), 1)

    def test_create_choice(self):
        data = {'question': self.question_1.pk, 'choice_text': '42'}
        response = self.client.post(reverse('choices'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Choice.objects.count(), 2)
    
    def test_update_choice(self):
        data = {'id': 1, 
                'choice_text': 'Čivava na straži',
                'votes': 0,
                'question': 1
                }
        response = self.client.put(reverse('choice-detail', kwargs={'pk': self.choice_1.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        choice_data = {'id': 1, 
                    'choice_text': 'Čivava na straži',
                    'votes': 0,
                    'question': 1}
        self.assertEqual(response.data, choice_data)

    def test_retrieve_choice(self):
        response = self.client.get(reverse('choice-detail', kwargs={'pk': self.choice_1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.question_1.pk)
    
    def test_delete_choice(self):
        response = self.client.delete(reverse('choice-detail', kwargs={'pk': self.choice_1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Choice.objects.count(), 0)





