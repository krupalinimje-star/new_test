from django.urls import path
from shinchan import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.login_api, name="login"),
]