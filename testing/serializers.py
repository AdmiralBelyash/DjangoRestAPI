from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Answers, Questions, Competence, Themes, Levels, TestingResult, TestSettings

from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token,
        }


class TokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['is_moderator'] = self.user.is_staff

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class UserSerializer(serializers.ModelSerializer):
    current_level = serializers.CharField(source='current_level.name')

    class Meta:
        model = User
        fields = ['pk', 'first_name', 'last_name', 'email', 'current_level', 'post', 'address', 'phone_number']


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['pk', 'answer', 'is_correct']


class QuestionsSerializer(serializers.ModelSerializer):
    answers = AnswersSerializer(many=True)
    level = serializers.CharField(source='level.name')
    theme = serializers.CharField(source='theme.name')

    class Meta:
        model = Questions
        fields = [
            'pk',
            'question',
            'type',
            'level',
            'theme',
            'answers',
        ]


class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = ['pk', 'competence']


class ThemesSerializer(serializers.ModelSerializer):
    competence = serializers.CharField(source='competence.competence')

    class Meta:
        model = Themes
        fields = ['pk', 'name', 'competence']

    def create(self, validated_data):
        validated_data['competence'] = Competence.objects.get(id=validated_data['competence']['competence'])
        return Themes.objects.create(**validated_data)


class TestingResultSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source='level.name')
    competence = serializers.CharField(source='competence.competence')
    correct_answers = serializers.SerializerMethodField()

    def get_correct_answers(self, obj):
        return obj.question_summary - obj.wrong_questions

    class Meta:
        model = TestingResult
        fields = [
            'user_id',
            'level',
            'competence',
            'test_id',
            'updated_date',
            'question_summary',
            'wrong_questions',
            'time_summary',
            'time_spent',
            'correct_answers'
        ]


class LevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Levels
        fields = '__all__'


class TestSettingsSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source='level_id.name', read_only=True)
    competence = serializers.CharField(source='competence_id.competence', read_only=True)

    class Meta:
        model = TestSettings
        fields = [
            'id',
            'name',
            'level',
            'level_id',
            'competence',
            'competence_id',
            'time',
            'next_level_score',
            'questions_count',
        ]
