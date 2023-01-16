from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.textPage, name='text'),
    path('quiz/<int:id>/', views.quiz, name='quiz'),
    path('mypage/', views.myPage, name='myPage'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]