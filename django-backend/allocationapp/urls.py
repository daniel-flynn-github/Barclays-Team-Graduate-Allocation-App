from django.urls import path

from . import views

app_name = 'allocationapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('cast_votes/', views.cast_votes, name='cast_votes'),
    path('vote_submitted/', views.vote_submitted, name="vote_submitted"),
    path('result_page/', views.result_page, name="result_page"),
    path('upload/', views.upload_file, name='upload'),
]