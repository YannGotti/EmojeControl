from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainPage.as_view()),
    path('game/', views.GamePage.as_view()),
]
