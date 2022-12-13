from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from testing import views
from testing.views import RegistrationAPIView, LoginAPIView, CreateQuestions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile', views.UserDetail.as_view()),
    path('me', views.UserRetrieveUpdateAPIView.as_view()),
    path('questions', views.QuestionsList.as_view()),
    path('questions/<int:pk>', views.QuestionsDetail.as_view()),
    path('themes', views.ThemeList.as_view()),
    path('themes/<int:pk>', views.ThemeDetail.as_view()),
    path('test_result', views.TestResultList.as_view()),
    path('test_result/last', views.LastResult.as_view()),
    path('test_result/<int:pk>', views.TestResultDetail.as_view()),
    path('competence', views.CompetenceList.as_view()),
    path('level', views.LevelList.as_view()),
    path('test', views.Test.as_view()),
    path('test_settings', views.TestSettingsListView.as_view()),
    path('test_settings/<int:pk>', views.TestSettingsDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('api/token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create_questions/', CreateQuestions.as_view(), name='create_questions')
]
