import datetime
import json
import jwt

from typing import Union, List, Dict

import django.utils.timezone
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import PermissionsMixin

from djangoRestApiTest import settings


class Levels(models.Model):
    name = models.CharField('Сложность', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Уровень сложности'
        verbose_name_plural = 'Уровни сложности'


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=256, default='Unknown')
    last_name = models.CharField(max_length=256, default='Unknown')
    post = models.CharField('Должность сотрудника', max_length=150, default='Unknown')
    phone_number = models.CharField('Номер телефона', max_length=12, unique=True, default='Unknown')
    address = models.CharField('Адрес сотрудника', max_length=150, default='Unknown')
    current_level = models.ForeignKey(Levels, on_delete=models.SET(2), default=2)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.datetime.now() + datetime.timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.encode('utf-8')


class Competence(models.Model):
    competence = models.CharField(
        'Название компетенции',
        max_length=300,
        unique=True,
        default='Unknown'
    )

    def __str__(self):
        return self.competence

    class Meta:
        verbose_name = 'Компетенция'
        verbose_name_plural = 'Компетенции'


class Themes(models.Model):
    name = models.CharField('Название темы', max_length=500,
                            help_text='Название темы')
    competence = models.ForeignKey(
        Competence,
        related_name='competence_theme',
        on_delete=models.CASCADE,
        default='Unknown'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


def f(value: Union[Dict, List]) -> None:
    if not isinstance(value, list):
        raise ValidationError('Should be array')

    for answer in value:
        if not isinstance(answer, dict):
            raise ValidationError('each answer should be dict')
        if 'is_correct' not in answer:
            raise ValidationError('no "is_correct"')
        if 'answer' not in answer:
            raise ValidationError('no "answer"')


class Questions(models.Model):
    question = models.TextField('Вопрос', max_length=3000, help_text='Текст вопроса', default='')
    theme = models.ForeignKey(
        Themes, on_delete=models.CASCADE,
        help_text='Тема вопроса'
    )
    competence = models.ForeignKey(
        Competence,
        on_delete=models.CASCADE,
        default=1
    )
    level = models.ForeignKey(
        Levels,
        on_delete=models.CASCADE,
        help_text='Сложность вопроса'
    )
    Type_Question = (
        ('1', 'Один ответ'),
        ('2', 'Несколько ответов')
    )
    type = models.CharField(
        max_length=1,
        choices=Type_Question,
        blank=True,
        default=1,
        help_text='Тип вопроса',
    )

    def display_theme(self):
        return self.theme.name

    display_theme.short_description = 'Theme'

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answers(models.Model):
    answer = models.TextField('Ответ', max_length=3000)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='answers')
    is_correct = models.BooleanField('Правильно или нет', default=False)

    def __str__(self):
        return self.answer

    def display_correct(self):
        return self.is_correct

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class TestSettings(models.Model):
    name = models.CharField(
        'Test name',
        max_length=200,
        default=f'Test'
    )
    level_id = models.ForeignKey(
        Levels,
        related_name='start_level',
        help_text='Начальный уровень сложности',
        on_delete=models.CASCADE,
        default=2
    )
    competence_id = models.ForeignKey(
        Competence,
        related_name='test_competence',
        help_text='Test Competence',
        on_delete=models.CASCADE,
        default='Unknown'
    )
    time = models.TimeField(
        'Время теста',
        default=datetime.time.fromisoformat('00:00:00')
    )
    next_level_score = models.IntegerField(
        'Количество баллов '
        'для перехода на следующий уровень',
        default=0
    )
    questions_count = models.IntegerField(
        'Questions in block count',
        default=0
    )

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    class Meta:
        verbose_name = 'Test Setting'
        verbose_name_plural = 'Test Settings'


class Courses(models.Model):
    theme = models.ForeignKey(
        Themes, related_name='theme',
        on_delete=models.CASCADE
    )
    level = models.ForeignKey(
        Levels, related_name='level',
        on_delete=models.CASCADE
    )
    link = models.CharField(
        'Ссылка на курс',
        max_length=200
    )

    class Meta:
        verbose_name = 'Курс для повышения квалификации'
        verbose_name_plural = 'Курсы для повышения квалификации'


class TestingResult(models.Model):
    user_id = models.ForeignKey(
        User,
        name='user_id',
        help_text='User ID',
        null=True,
        on_delete=models.CASCADE
    )
    test_id = models.ForeignKey(
        TestSettings,
        name='test_id',
        null=True,
        on_delete=models.CASCADE,
    )
    updated_time = models.DateTimeField(
        name='updated_date',
        default=django.utils.timezone.now
    )
    all_questions = models.IntegerField(
        name='question_summary',
        default=0,
        help_text='All questions count'
    )
    wrong_questions = models.IntegerField(
        name='wrong_questions',
        default=0,
        help_text='Wrong answers count'
    )
    skipped_questions = models.IntegerField(
        name='skipped_question_summary',
        default=0,
        help_text='Skipped questions count',
        null=True,
    )
    time_summary = models.DurationField(
        name='time_summary',
        null=True,
        help_text='Estimated Time'
    )
    time_spent = models.DurationField(
        name='time_spent',
        null=True,
        help_text='Time spent'
    )
    answered_questions = models.CharField(
        name='answered_questions',
        null=True,
        help_text='Questions answered by user',
        max_length=256,
    )
    competence = models.ForeignKey(
        Competence,
        name='competence',
        default=1,
        on_delete=models.CASCADE
    )
    level = models.ForeignKey(
        Levels,
        name='level',
        default=2,
        on_delete=models.CASCADE
    )

    def set_answered_questions(self, questions):
        question_ids = []
        for question in questions:
            question_ids.append(question.id)
        self.answered_questions = json.dumps(question_ids)

    def get_answered_questions(self):
        return json.loads(self.answered_questions)

    def clear_answered_questions(self):
        print(f'Clearing answered questions for user {self.user_id.id}')
        self.answered_questions = json.dumps('')

    class Meta:
        verbose_name = 'Результат тестирования'
        verbose_name_plural = 'Результаты тестирования'
