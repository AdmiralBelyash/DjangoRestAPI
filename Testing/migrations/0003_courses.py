# Generated by Django 4.0.3 on 2022-03-30 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Testing', '0002_alter_answers_question_alter_questions_level_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=200, verbose_name='Ссылка на курс')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='level', to='Testing.levels')),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='theme', to='Testing.themes')),
            ],
            options={
                'verbose_name': 'Курс для повышения квалификации',
                'verbose_name_plural': 'Курсы для повышения квалификации',
            },
        ),
    ]
