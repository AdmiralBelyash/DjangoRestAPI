import datetime
from typing import Union, List, Dict

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Levels(models.Model):
    name = models.CharField("Сложность", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Уровень сложности"
        verbose_name_plural = "Уровни сложности"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post = models.CharField("Должность сотрудника", max_length=150, default="Unknown")
    phone_number = models.CharField("Номер телефона", max_length=12, unique=True, default="Unknown")
    address = models.CharField("Адрес сотрудника", max_length=150, default="Unknown")
    current_level = models.ForeignKey(Levels, on_delete=models.SET(2))

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class Competence(models.Model):
    competence = models.CharField("Название компетенции", max_length=300,
                                  unique=True, default="Unknown")

    def __str__(self):
        return self.competence

    class Meta:
        verbose_name = "Компетенция"
        verbose_name_plural = "Компетенции"


class Themes(models.Model):
    name = models.CharField("Название темы", max_length=500,
                            help_text="Название темы")
    competence = models.ForeignKey(Competence,
                                   related_name="competence_theme",
                                   on_delete=models.SET_DEFAULT,
                                   default="Unknown")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"


def f(value: Union[Dict, List]) -> None:
    if not isinstance(value, list):
        raise ValidationError("Should be array")

    for answer in value:
        if not isinstance(answer, dict):
            raise ValidationError("each answer should be dict")
        if "is_correct" not in answer:
            raise ValidationError("no 'is_correct'")
        if "answer" not in answer:
            raise ValidationError("no 'answer'")


class Questions(models.Model):
    question = models.TextField("Вопрос", max_length=3000, help_text="Текст вопроса", default='')
    theme = models.ForeignKey(Themes, on_delete=models.CASCADE,
                              help_text="Тема вопроса")
    level = models.ForeignKey(Levels, on_delete=models.CASCADE,
                              help_text="Сложность вопроса")
    Type_Question = (
        ('1', 'Один ответ'),
        ('2', 'Несколько ответов')
    )
    type = models.CharField(
        max_length=1,
        choices=Type_Question,
        blank=True,
        default=1,
        help_text="Тип вопроса",
    )

    def display_theme(self):
        return self.theme.name

    display_theme.short_description = 'Theme'

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answers(models.Model):
    answer = models.TextField("Ответ", max_length=3000)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name="answers")
    is_correct = models.BooleanField("Правильно или нет", default=False)

    def __str__(self):
        return self.answer

    def display_correct(self):
        return self.is_correct

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class UserAnswer(models.Model):
    user = models.ForeignKey(User, related_name="user_answer", on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answers, related_name="user_answer")
    question = models.OneToOneField(Questions, related_name="user_question", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователя"


class Testing(models.Model):
    user = models.ForeignKey(User, related_name="testing_user",
                            on_delete=models.CASCADE)
    question = models.ManyToManyField(Questions,
                            related_name="testing_question")
    level = models.ForeignKey(Levels, related_name="start_level",
                            help_text="Начальный уровень сложности",
                            on_delete=models.CASCADE,
                            default=2)
    themes = models.ManyToManyField(Themes, related_name="themes",
                            help_text="Набор тем для теста", default=None)
    time = models.TimeField("Время теста",
                            default=datetime.time.fromisoformat("00:00:00"))
    answers_pass_value = models.IntegerField \
        ("Количество вопросов для перехода на следующий уровень",
                            default=0)
    next_level_score = models.IntegerField("Количество баллов "
                            "для перехода на следующий уровень"
                            , default=0)

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class Courses(models.Model):
    theme = models.ForeignKey(Themes, related_name="theme",
                              on_delete=models.CASCADE)
    level = models.ForeignKey(Levels, related_name="level",
                              on_delete=models.CASCADE)
    link = models.CharField("Ссылка на курс", max_length=200)

    class Meta:
        verbose_name = "Курс для повышения квалификации"
        verbose_name_plural = "Курсы для повышения квалификации"
