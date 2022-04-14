from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from .models import UserAnswer, Answers, Questions, Testing, Competence, Themes, Levels
from django.contrib.auth.models import User, Group
from . import serializers


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class TestingList(generics.ListCreateAPIView):
    queryset = Testing.objects.all()
    serializer_class = serializers.TestingSerializer


class TestingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Testing.objects.all()
    serializer_class = serializers.TestingSerializer


class QuestionsList(generics.ListCreateAPIView):
    queryset = Questions.objects.all()
    serializer_class = serializers.QuestionsSerializer


class QuestionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Questions.objects.all()
    serializer_class = serializers.QuestionsSerializer


class ThemeList(generics.ListCreateAPIView):
    queryset = Themes.objects.all()
    serializer_class = serializers.ThemesSerializer


class ThemeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Themes.objects.all()
    serializer_class = serializers.ThemesSerializer


