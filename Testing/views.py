from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User, UserAnswer, Answers, Questions, Testing, Competence, Roles, Themes, Levels
from .serializers import *


@api_view(['GET', 'POST'])
def users_list(request):
    """
    List users, or create a new user
    """
    if request.method == 'GET':
        data = []
        next_page = 1
        previous_page = 1
        users = User.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(users, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = UserSerializer(data, context={'request': request}, many=True)
        if data.has_next():
            next_page = data.next_page_number()
        if data.has_previous():
            previous_page = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count, 'numpages': paginator.num_pages,
                         'nextlink': '/api/users/?page=' + str(next_page),
                         'prevlink': '/api/users/?page=' + str(previous_page)})

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def users_detail(request, pk):
    """
    Retrieve, update or delete a user by id/pk.
    """

    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def testing_list(request):
    """
    List users, or create a new test
    """
    if request.method == 'GET':
        data = []
        next_page = 1
        previous_page = 1
        testing = Testing.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(testing, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = TestingSerializer(data, context={'request': request}, many=True)
        if data.has_next():
            next_page = data.next_page_number()
        if data.has_previous():
            previous_page = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count, 'numpages': paginator.num_pages,
                         'nextlink': '/api/testing/?page=' + str(next_page),
                         'prevlink': '/api/testing/?page=' + str(previous_page)})

    elif request.method == 'POST':
        serializer = TestingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def testing_detail(request, pk):
    """
    Retrieve, update or delete a testing by id/pk.
    """
    try:
        testing = Testing.objects.get(pk=pk)
    except Testing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TestingSerializer(testing, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TestingSerializer(testing, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        testing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def questions_list(request):
    """
    List questions, or create a new question
    """
    if request.method == 'GET':
        data = []
        next_page = 1
        previous_page = 1
        questions = Questions.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(questions, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = QuestionsSerializer(data, context={'request': request}, many=True)
        if data.has_next():
            next_page = data.next_page_number()
        if data.has_previous():
            previous_page = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count, 'numpages': paginator.num_pages,
                        'nextlink': '/api/questions/?page=' + str(next_page),
                         'prevlink': '/api/questions/?page=' + str(previous_page)})

    elif request.method == 'POST':
        serializer = QuestionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def questions_detail(request, pk):
    """
    Retrieve, update or delete a question by id/pk.
    """

    try:
        questions = Questions.objects.get(pk=pk)
    except Questions.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = QuestionsSerializer(questions, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = QuestionsSerializer(questions, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        questions.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def theme_list(request):
    """
    List themes, or create a new theme
    """
    if request.method == 'GET':
        data = []
        next_page = 1
        previous_page = 1
        themes = Themes.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(themes, 30)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = ThemesSerializer(data, context={'request': request}, many=True)
        if data.has_next():
            next_page = data.next_page_number()
        if data.has_previous():
            previous_page = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count, 'numpages': paginator.num_pages,
                        'nextlink': '/api/questions/?page=' + str(next_page),
                         'prevlink': '/api/questions/?page=' + str(previous_page)})

    elif request.method == 'POST':
        serializer = ThemesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def theme_detail(request, pk):
    """
    Retrieve, update or delete a theme by id/pk.
    """

    try:
        themes = Themes.objects.get(pk=pk)
    except Themes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ThemesSerializer(themes, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ThemesSerializer(themes, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        themes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def questions_theme(request, pk):
    try:
        questions = Questions.objects.all().filter(theme_id=pk)
    except Questions.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = QuestionsSerializer(questions, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def test_algorithm(request, pk):
    if int(pk) == 0:
        try:
            questions = Questions.objects.all()[:3]
        except Questions.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionsSerializer(questions, context={'request': request}, many=True)
        return Response(serializer.data)

    correct_answers = int(pk) // 100
    id_theme = int((int(pk) / 10) % 10)
    id_level = int(pk) % 10
    if id_level == 3:
        id_theme += 1
        try:
            questions = Questions.objects.all().filter(level_id=2, theme_id=id_theme)
        except Questions.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionsSerializer(questions, context={'request': request}, many=True)
        return Response(serializer.data)

    else:
        if correct_answers >= 2:
            id_level += 1
            try:
                questions = Questions.objects.all().filter(level_id=id_level, theme_id=id_theme)
            except Questions.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = QuestionsSerializer(questions, context={'request': request}, many=True)
            return Response(serializer.data)
        else:
            id_level -= 1
            try:
                questions = Questions.objects.all().filter(level_id=id_level, theme_id=id_theme)
            except Questions.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = QuestionsSerializer(questions, context={'request': request}, many=True)
            return Response(serializer.data)


