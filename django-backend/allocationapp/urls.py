from django.urls import path

from . import views

app_name = 'allocationapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('cast_votes/', views.cast_votes, name='cast_votes'),
    path('graduate_login/', views.graduate_login, name='graduate_login'),
    path('login_landing/', views.login_landing, name="login_landing"),
]