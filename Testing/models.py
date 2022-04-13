from typing import Union, List, Dict

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Roles(models.Model):
    """Роли"""
    permission = models.CharField("Название роли", max_length=30)

    def __str__(self):
        return self.permission

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"


class User(models.Model):
    """Пользователь"""
    email = models.EmailField("Почта", max_length=150)
    name = models.CharField("Полное имя", max_length=150)
    hash_password = models.CharField("Хэш пароля", max_length=500)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, default=3)

    def __str__(self):
        return self.name

    def display_email(self):
        return self.email
    display_email.short_description = 'email'

    def display_role(self):
        return self.role.permission
    display_role.short_description = 'permission'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Competence(models.Model):
    """Компетенции"""
    competence = models.CharField("Название компетенции", max_length=300, unique=True, default="Unknown")

    def __str__(self):
        return self.competence

    class Meta:
        verbose_name = "Компетенция"
        verbose_name_plural = "Компетенции"


class Themes(models.Model):
    """Темы"""
    name = models.CharField("Название темы", max_length=500, help_text="Название темы")
    competence = models.ForeignKey(Competence,
                                   related_name="competence_theme",
                                   on_delete=models.SET_DEFAULT,
                                   default="Unknown")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"


class Levels(models.Model):
    """Уровни сложности"""
    name = models.CharField("Сложность", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Уровень сложности"
        verbose_name_plural = "Уровни сложности"


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
    """Вопросы"""
    question = models.TextField("Вопрос", max_length=3000, help_text="Текст вопроса", default='')
    theme = models.ForeignKey(Themes, on_delete=models.CASCADE,
                              help_text="Тема вопроса")
    level = models.ForeignKey(Levels, on_delete=models.CASCADE,
                              help_text="Сложность вопроса")
    # answers = models.JSONField(default=dict, validators=[f])
    '''[
        {
            "is_correct": true,
            "answer": "sdasgasdgasdgagsd"
        },
        {
            "is_correct": false,
            "answer": "sdasgasdgasdgagsd"
        },
        {
            "is_correct": false,
            "answer": "sdasgasdgasdgagsd"
        }
    ]'''

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
    """Ответы"""
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
    """Ответ пользователя"""
    user = models.ForeignKey(User, related_name="user_answer", on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answers, related_name="user_answer")
    question = models.OneToOneField(Questions, related_name="user_question", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователя"


class Testing(models.Model):
    """Тестирование"""
    user = models.ForeignKey(User, related_name="testing_user", on_delete=models.CASCADE)
    question = models.ManyToManyField(Questions, related_name="testing_question")

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"




class Courses(models.Model):
    """Курсы"""
    theme = models.ForeignKey(Themes, related_name="theme", on_delete=models.CASCADE)
    level = models.ForeignKey(Levels, related_name="level", on_delete=models.CASCADE)
    link = models.CharField("Ссылка на курс", max_length = 200)
    
    
    class Meta:
        verbose_name = "Курс для повышения квалификации"
        verbose_name_plural = "Курсы для повышения квалификации"