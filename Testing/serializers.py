from rest_framework import serializers
from .models import User, UserAnswer, Answers, Questions, Testing, Competence, Roles, Themes, Levels


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('pk', 'name', 'email', 'hash_password', 'role')


class AnswersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answers
        fields = "__all__"


class QuestionsSerializer(serializers.ModelSerializer):
    # theme = serializers.SlugRelatedField(slug_field="name", read_only=True)
    # level = serializers.SlugRelatedField(slug_field="name", read_only=True)
    answers = AnswersSerializer(many=True)

    class Meta:
        model = Questions
        fields = ('pk', 'question', 'type', 'level', 'theme', 'answers')


class TestingSerializer(serializers.ModelSerializer):
    # question = serializers.SlugRelatedField(slug_field="question", read_only=True, many=True)
    question = QuestionsSerializer(many=True)

    class Meta:
        model = Testing
        fields = ('pk', 'user', 'question')


class CompetenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competence
        fields = "__all__"


class ThemesSerializer(serializers.ModelSerializer):
    competence = serializers.SlugRelatedField(slug_field="competence", read_only=True)

    class Meta:
        model = Themes
        fields = "__all__"
