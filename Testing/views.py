import random

from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Questions, Testing, Themes, Levels, Profile, TestingResult


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
    queryset = Questions.objects.all()
    serializer_class = serializers.QuestionsSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        new_question = Questions.objects.create(
            question=data['question'],
            theme=Themes(data['theme']),
            level=Levels(data['level']),
            type=data['type']
        )
        serializer = serializers.QuestionsSerializer(new_question)
        return Response(serializer.data)


class QuestionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Questions.objects.all()
    serializer_class = serializers.QuestionsSerializer

    def destroy(self, request, *args, **kwargs):
        question_object = self.get_object()
        question_object.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        question_object = self.get_object()
        data = request.data

        question_object.question = data['question']
        question_object.theme = Themes(data['theme'])
        question_object.level = Levels(data['level'])

        question_object.save()
        serializer = serializers.QuestionsSerializer(question_object)
        return Response(serializer.data)


class ThemeList(generics.ListCreateAPIView):
    queryset = Themes.objects.all()
    serializer_class = serializers.ThemesSerializer


class ThemeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Themes.objects.all()
    serializer_class = serializers.ThemesSerializer


class TestingAlgorithm(generics.RetrieveUpdateAPIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.response = request.data
        self.questions_count = 0
        self.selected_questions_id = []

    def get_level(self):
        level = self.response['level']
        return level

    def get_theme(self):
        competence = self.response['competence']
        selected_themes_id = []
        for themes_id in Themes.objects.filter(competence=competence):
            selected_themes_id.append(themes_id.id)
        theme = selected_themes_id[random.randrange(len(selected_themes_id))]
        return theme

    def get_start_questions(self):
        for question_id in Questions.objects.filter(level=self.get_level(), theme=self.get_theme()):
            self.selected_questions_id.append(question_id.pk)
        pk = self.selected_questions_id[random.randrange(len(self.selected_questions_id))]
        yield Questions.objects.filter(pk=pk)
        self.selected_questions_id.remove(int(pk))

    def get_question(self):
        # if self.questions_count < 3:
        #     serializer = serializers.QuestionsSerializer(self.get_start_questions())
        #     self.questions_count += 1
        #     return Response(serializer.data)
        # else:
        for question_id in Questions.objects.filter(level=2, theme=2):
            self.selected_questions_id.append(question_id.pk)
        pk = self.selected_questions_id[random.randrange(len(self.selected_questions_id))]
        serializer = serializers.QuestionsSerializer(Questions.objects.filter(pk=pk))
        self.selected_questions_id.remove(int(pk))
        self.questions_count += 1
        return Questions.objects.filter(pk=pk)


class Test(generics.ListAPIView):
    testing = TestingAlgorithm()
    queryset = testing.get_question()
    serializer_class = serializers.QuestionsSerializer


class TestResultList(generics.ListCreateAPIView):
    queryset = TestingResult.objects.all()
    serializer_class = serializers.TestingResultSerializer


class TestResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestingResult.objects.all()
    serializer_class = serializers.TestingResultSerializer

    def destroy(self, request, *args, **kwargs):
        test_result_obj = self.get_object()
        test_result_obj.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        testing_result_object = self.get_object()
        data = request.data

        testing_result_object.user_id = data['user_id']
        testing_result_object.updated_time = data['updated_time']
        testing_result_object.all_questions = data['all_questions']
        testing_result_object.wrong_questions = data['wrong_questions']
        testing_result_object.skipped_questions = data['skipped_questions']
        testing_result_object.time_summary = data['time_summary']
        testing_result_object.time_spent = data['time_spent']

        testing_result_object.save()

        serializer = serializers.QuestionsSerializer(testing_result_object)
        return Response(serializer.data)
