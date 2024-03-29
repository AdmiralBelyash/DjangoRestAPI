# Generated by Django 4.0.4 on 2022-11-09 15:20

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competence', models.CharField(default='Unknown', max_length=300, unique=True, verbose_name='Название компетенции')),
            ],
            options={
                'verbose_name': 'Компетенция',
                'verbose_name_plural': 'Компетенции',
            },
        ),
        migrations.CreateModel(
            name='Levels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Сложность')),
            ],
            options={
                'verbose_name': 'Уровень сложности',
                'verbose_name_plural': 'Уровни сложности',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(db_index=True, max_length=255, unique=True)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(default='Unknown', max_length=256)),
                ('last_name', models.CharField(default='Unknown', max_length=256)),
                ('post', models.CharField(default='Unknown', max_length=150, verbose_name='Должность сотрудника')),
                ('phone_number', models.CharField(default='Unknown', max_length=12, unique=True, verbose_name='Номер телефона')),
                ('address', models.CharField(default='Unknown', max_length=150, verbose_name='Адрес сотрудника')),
                ('current_level', models.ForeignKey(default=2, on_delete=models.SET(2), to='testing.levels')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Themes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название темы', max_length=500, verbose_name='Название темы')),
                ('competence', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.CASCADE, related_name='competence_theme', to='testing.competence')),
            ],
            options={
                'verbose_name': 'Тема',
                'verbose_name_plural': 'Темы',
            },
        ),
        migrations.CreateModel(
            name='TestSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Test', max_length=200, verbose_name='Test name')),
                ('time', models.TimeField(default=datetime.time(0, 0), verbose_name='Время теста')),
                ('next_level_score', models.IntegerField(default=0, verbose_name='Количество баллов для перехода на следующий уровень')),
                ('questions_count', models.IntegerField(default=0, verbose_name='Questions in block count')),
                ('competence', models.ForeignKey(default='Unknown', help_text='Test Competence', on_delete=django.db.models.deletion.CASCADE, related_name='test_competence', to='testing.competence')),
                ('level', models.ForeignKey(default=2, help_text='Начальный уровень сложности', on_delete=django.db.models.deletion.CASCADE, related_name='start_level', to='testing.levels')),
            ],
            options={
                'verbose_name': 'Test Setting',
                'verbose_name_plural': 'Test Settings',
            },
        ),
        migrations.CreateModel(
            name='TestingResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('question_summary', models.IntegerField(default=0, help_text='All questions count')),
                ('wrong_questions', models.IntegerField(default=0, help_text='Wrong answers count')),
                ('skipped_question_summary', models.IntegerField(default=0, help_text='Skipped questions count', null=True)),
                ('time_summary', models.DurationField(help_text='Estimated Time', null=True)),
                ('time_spent', models.DurationField(help_text='Time spent', null=True)),
                ('answered_questions', models.CharField(help_text='Questions answered by user', max_length=256, null=True)),
                ('competence', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='testing.competence')),
                ('level', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='testing.levels')),
                ('user_id', models.ForeignKey(help_text='User ID', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Результат тестирования',
                'verbose_name_plural': 'Результаты тестирования',
            },
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(default='', help_text='Текст вопроса', max_length=3000, verbose_name='Вопрос')),
                ('type', models.CharField(blank=True, choices=[('1', 'Один ответ'), ('2', 'Несколько ответов')], default=1, help_text='Тип вопроса', max_length=1)),
                ('competence', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='testing.competence')),
                ('level', models.ForeignKey(help_text='Сложность вопроса', on_delete=django.db.models.deletion.CASCADE, to='testing.levels')),
                ('theme', models.ForeignKey(help_text='Тема вопроса', on_delete=django.db.models.deletion.CASCADE, to='testing.themes')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=200, verbose_name='Ссылка на курс')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='level', to='testing.levels')),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='theme', to='testing.themes')),
            ],
            options={
                'verbose_name': 'Курс для повышения квалификации',
                'verbose_name_plural': 'Курсы для повышения квалификации',
            },
        ),
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(max_length=3000, verbose_name='Ответ')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Правильно или нет')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='testing.questions')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
    ]
