import random
from typing import Any

from django.contrib.auth.models import User
from rest_framework import generics, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Questions, Testing, Themes, Levels, Profile, TestingResult, Competence


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def destroy(self, request, *args, **kwargs):
        profile_object = self.get_object()
        profile_object.user.delete()
        profile_object.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        profile_object = self.get_object()
        data = request.data

        profile_object.post = data['post']
        profile_object.user.first_name = data['user']['first_name']
        profile_object.user.last_name = data['user']['last_name']
        profile_object.user.email = data['user']['email']
        profile_object.phone_number = data['phone_number']
        profile_object.address = data['address']
        profile_object.current_level = Levels(data['current_level'])

        profile_object.save()
        profile_object.user.save()
        serializer = serializers.ProfileSerializer(profile_object)

        return Response(serializer.data)


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
    serializer_class = serializers.QuestionsSerializer
    queryset = Questions.objects.all()


class QuestionByThemeViewSet(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.QuestionsSerializer
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Questions.objects.all()
        theme = self.request.query_params.get('theme', None)
        if theme is not None:
            queryset = queryset.filter(theme_id=theme)
        return queryset


class QuestionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Questions.objects.all()
    serializer_class = serializers.QuestionsSerializer


class ThemeList(generics.ListCreateAPIView):
    queryset = Themes.objects.all()
    serializer_class = serializers.ThemesSerializer


class CompetenceList(generics.ListCreateAPIView):
    queryset = Competence.objects.all()
    serializer_class = serializers.CompetenceSerializer


class CompetenceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Competence.objects.all()
    serializer_class = serializers.CompetenceSerializer


class ThemeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Themes.objects.all()
    serializer_class = serializers.ThemesSerializer


class TestResultList(generics.ListCreateAPIView):
    queryset = TestingResult.objects.all()
    serializer_class = serializers.TestingResultSerializer

    def get(self, request, *args, **kwargs):
        results = TestingResult.objects.filter(
            user_id=request.GET.get('user')
        )
        serializer = serializers.TestingResultSerializer(results, many=True)
        return Response(serializer.data)


class TestResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestingResult.objects.all()
    serializer_class = serializers.TestingResultSerializer
