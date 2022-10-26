from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from Testing import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile', views.UserDetail.as_view()),
    path('questions', views.QuestionsList.as_view()),
    path('questions/<int:pk>', views.QuestionsDetail.as_view()),
    path('themes', views.ThemeList.as_view()),
    path('themes/<int:pk>', views.ThemeDetail.as_view()),
    path('test_result', views.TestResultList.as_view()),
    path('test_result/<int:pk>', views.TestResultDetail.as_view()),
    path('competence', views.CompetenceList.as_view()),
    path('level', views.LevelList.as_view()),
    path('test', views.Test.as_view()),
    path('test_settings', views.TestSettingsListView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('auth/', include('django.contrib.auth.urls')),
]
