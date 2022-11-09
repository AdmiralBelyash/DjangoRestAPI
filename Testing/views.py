from django.template.loaders import cached
from rest_framework import generics, status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import (
    Questions,
    Themes,
    Levels,
    User,
    TestingResult,
    Competence,
    TestSettings,
)
from .renderers import UserJSONRenderer
from .serializers import TestSettingsSerializer, RegistrationSerializer, LoginSerializer, UserSerializer
from .testing_algorithm import TestAlgorithm


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def destroy(self, request, *args, **kwargs):
        profile_object = self.get_object()
        profile_object.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        profile_object = self.get_object()
        data = request.data

        profile_object.post = data['post']
        profile_object.first_name = data['user']['first_name']
        profile_object.last_name = data['user']['last_name']
        profile_object.email = data['user']['email']
        profile_object.phone_number = data['phone_number']
        profile_object.address = data['address']

        profile_object.save()
        serializer = serializers.UserSerializer(profile_object)

        return Response(serializer.data)


class QuestionsList(generics.ListCreateAPIView):
    queryset = Questions.objects.all()
    serializer_class = serializers.QuestionsSerializer

    def get(self, request, *args, **kwargs):
        if request.GET.get('level'):
            questions = Questions.objects.filter(
                level__pk=request.GET.get('level'),
                theme__competence_id=request.GET.get('competence')
            )
            serializer = serializers.QuestionsSerializer(questions, many=True)
            return Response(serializer.data)
        questions = Questions.objects.filter(
            theme__pk=request.GET.get('theme')
        )
        serializer = serializers.QuestionsSerializer(questions, many=True)
        return Response(serializer.data)

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

    def delete(self, request, *args, **kwargs):
        questions_to_delete = Questions.objects.filter(
            id__in=request.data,
        )
        questions_to_delete.delete()
        return Response(status=status.HTTP_200_OK)


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

    def get(self, request, *args, **kwargs):
        if request.GET.get('competence'):
            themes = Themes.objects.filter(
                competence_id=request.GET.get('competence')
            )
            serializer = serializers.ThemesSerializer(themes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        themes = Themes.objects.all()
        serializer = serializers.ThemesSerializer(themes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        themes_to_delete = Themes.objects.filter(
            id__in=request.data,
        )
        themes_to_delete.delete()
        return Response(status=status.HTTP_200_OK)


class CompetenceList(generics.ListCreateAPIView):
    queryset = Competence.objects.all()
    serializer_class = serializers.CompetenceSerializer

    def delete(self, request, *args, **kwargs):
        competence_to_delete = Competence.objects.filter(
            id__in=request.data,
        )
        competence_to_delete.delete()
        return Response(status=status.HTTP_200_OK)


class CompetenceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Competence.objects.all()
    serializer_class = serializers.CompetenceSerializer


class ThemeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Themes.objects.all()
    serializer_class = serializers.ThemesSerializer


class LevelList(generics.ListCreateAPIView):
    queryset = Levels.objects.all()
    serializer_class = serializers.LevelsSerializer


class TestResultList(generics.ListCreateAPIView):
    queryset = TestingResult.objects.all()
    serializer_class = serializers.TestingResultSerializer

    def get(self, request, *args, **kwargs):
        results = TestingResult.objects.filter(
            user_id_id=request.GET.get('user')
        )
        serializer = serializers.TestingResultSerializer(results, many=True)
        return Response(serializer.data)


class TestResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestingResult.objects.all()
    serializer_class = serializers.TestingResultSerializer


class Test(APIView):
    permission_classes = (IsAuthenticated,)
    #renderer_classes = (UserJSONRenderer,)
    level = None

    def get(self, request):
        questions, level = self.testing_algorithm.get_start_questions()
        self.level = level
        print(self.level, 'One')
        serializer = serializers.QuestionsSerializer(questions, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        next_level = False

        if request.data.get('answers'):
            self.testing_algorithm.calculate_statistic(
                answers_ids=request.data['answers']
            )
            next_level = self.testing_algorithm.is_next_level()

        print(self.level, 'Two')
        questions, level = self.testing_algorithm.get_questions(next_level)
        self.level = level
        print(self.level, 'Three')
        serializer = serializers.QuestionsSerializer(questions, many=True)

        yield Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    @property
    def test_settings(self):
        return TestSettings.objects.get(
            id=self.request.GET.get('id')
        )

    @property
    def testing_algorithm(self):
        return TestAlgorithm(
            self.test_settings,
            self.request.user
        )


class TestSettingsListView(generics.GenericAPIView):
    serializer_class = TestSettingsSerializer
    queryset = TestSettings.objects.all()

    def get(self, request):
        test_settings = TestSettings.objects.all()
        serializer = TestSettingsSerializer(test_settings, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        data = request.data
        TestSettings.objects.create(
            competence=Competence(data['competence']),
            level=Levels(data['level']),
            time=data['testTime'],
            questions_count=data['questionsCount'],
            next_level_score=data['thresholdScore'],
            name=data['testName']
        )

        return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        test_settings = self.get_object()
        data = request.data

        test_settings.name = data['name']
        test_settings.level = Levels(data['level'])
        test_settings.competence = Competence(data['competence'])
        test_settings.time = data['testTime']
        test_settings.next_level_score = data['thresholdScore']
        test_settings.questions_count = data['questionsCount']

        test_settings.save()

        return Response(status=status.HTTP_200_OK)


class TestSettingsDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestSettingsSerializer
    queryset = TestSettings.objects.all()
