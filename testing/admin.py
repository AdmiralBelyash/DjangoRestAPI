from django.contrib import admin
from .models import(
    Answers,
    Questions,
    Competence,
    Themes,
    Levels,
    Courses,
    User,
    TestSettings,
    TestingResult,
)

admin.site.register(Competence)
admin.site.register(Themes)
admin.site.register(Levels)
admin.site.register(Courses)
admin.site.register(User)
admin.site.register(TestSettings)
admin.site.register(TestingResult)


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
