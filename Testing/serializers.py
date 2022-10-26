from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Answers, Questions, Competence, Themes, Levels, Profile, TestingResult, TestSettings
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'first_name', 'last_name', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    current_level = serializers.CharField(source='current_level.name')

    class Meta:
        model = Profile
        fields = "__all__"


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


class TestingResultSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source='level.name')
    competence = serializers.CharField(source='competence.competence')

    class Meta:
        model = TestingResult
        fields = [
            'user_id',
            'level',
            'competence',
            'updated_time',
            'all_questions',
            'wrong_questions',
            'skipped_questions',
            'time_summary',
            'answered_questions',
        ]


class LevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Levels
        fields = '__all__'


class TestSettingsSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source='level.name')
    competence = serializers.CharField(source='competence.competence')

    class Meta:
        model = TestSettings
        fields = [
            'id',
            'name',
            'level',
            'competence',
            'time',
            'next_level_score',
            'questions_count',
        ]


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
            # We have a valid user, put it in the serializer's validated_data.
            # It will be used in the view.
        attrs['user'] = user
        return attrs
