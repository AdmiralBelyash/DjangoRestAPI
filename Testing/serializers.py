from rest_framework import serializers
from .models import UserAnswer, Answers, Questions, Competence, Themes, Levels, Profile, TestingResult, TestSettings
from django.contrib.auth.models import User, Group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'first_name', 'last_name', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields = "__all__"


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['pk', 'answer', 'is_correct']


class QuestionsSerializer(serializers.ModelSerializer):
    answers = AnswersSerializer(many=True)

    class Meta:
        model = Questions
        fields = ['pk', 'question', 'type', 'level', 'theme', 'answers']


class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = ['pk', 'competence']


class ThemesSerializer(serializers.ModelSerializer):
    competence = serializers.RelatedField

    class Meta:
        model = Themes
        fields = ['pk', 'name', 'competence']


class TestingResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestingResult
        fields = '__all__'


class LevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Levels
        fields = '__all__'


class TestSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestSettings
        fields = '__all__'
