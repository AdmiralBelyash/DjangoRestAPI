from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from Testing import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('testing/', views.TestingList.as_view()),
    path('testing/<int:pk>/', views.TestingDetail.as_view()),
    path('questions/', views.QuestionsList.as_view()),
    path('questions/<int:pk>/', views.QuestionsDetail.as_view()),
    path('themes/', views.ThemeList.as_view()),
    path('themes/<int:pk>/', views.ThemeDetail.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/token/', obtain_auth_token, name='token'),
    path('api-auth/', include('rest_framework.urls')),
    path('test_result', views.TestResultList.as_view()),
    path('test_result/<int:pk>/', views.TestResultDetail.as_view()),
]

