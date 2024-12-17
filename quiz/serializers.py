from rest_framework import serializers

from quiz.models import Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, source='choice_set', required=False)  # Nested serializer

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('owner',)
