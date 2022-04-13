from django.contrib import admin
from .models import User, UserAnswer, Answers, Questions, Testing, Competence, Roles, Themes, Levels, Courses

# admin.site.register(User)
admin.site.register(UserAnswer)
# admin.site.register(Answers)
# admin.site.register(Questions)
admin.site.register(Competence)
admin.site.register(Roles)
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


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_email', 'display_role')


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ('question', 'id', 'display_correct')
    list_filter = ['is_correct']
