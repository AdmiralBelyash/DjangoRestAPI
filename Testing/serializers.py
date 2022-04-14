from rest_framework import serializers
from .models import UserAnswer, Answers, Questions, Testing, Competence, Themes, Levels
from django.contrib.auth.models import User, Group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = "__all__"


class QuestionsSerializer(serializers.ModelSerializer):
    answers = AnswersSerializer(many=True)

    class Meta:
        model = Questions
        fields = ['pk', 'question', 'type', 'level', 'theme', 'answers']


class TestingSerializer(serializers.ModelSerializer):
    question = QuestionsSerializer(many=True)

    class Meta:
        model = Testing
        fields = ['id', 'question', 'time']


class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = "__all__"


class ThemesSerializer(serializers.ModelSerializer):
    competence = serializers.SlugRelatedField(slug_field="competence", read_only=True)

    class Meta:
        model = Themes
        fields = "__all__"
