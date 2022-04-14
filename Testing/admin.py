from django.contrib import admin
from .models import UserAnswer, Answers, Questions, Testing, Competence, Themes, Levels, Courses
from django.contrib.auth.models import User, Group

admin.site.register(UserAnswer)
# admin.site.register(Answers)
# admin.site.register(Questions)
admin.site.register(Competence)
admin.site.register(Themes)
admin.site.register(Levels)
admin.site.register(Testing)
admin.site.register(Courses)


class AnswerInline(admin.TabularInline):
    model = Answers


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_theme', 'level')
    list_filter = ['level']
    inlines = [AnswerInline]


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ('question', 'id', 'display_correct')
    list_filter = ['is_correct']
