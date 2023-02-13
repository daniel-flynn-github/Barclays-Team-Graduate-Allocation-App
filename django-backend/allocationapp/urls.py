from django.urls import path

from . import views

app_name = 'allocationapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('cast_votes/', views.cast_votes, name='cast_votes'),
    path('vote_submitted/', views.vote_submitted, name="vote_submitted"),
    path('result_page/', views.result_page, name="result_page"),
    path('get_allocation/', views.get_allocation, name="get_allocation"),
    path('manager_view_teams/', views.manager_view_teams, name='manager_view_teams'),
    path('edit_team/<int:team_id>/', views.manager_edit_team, name='manager_edit_team'),
    path('delete_team_member/<int:user_id>/', views.delete_team_member, name='delete_team_member'),
    path('create_new_team/',views.create_new_team, name = 'create_new_team'),
    path('upload/', views.upload_file, name='upload'),
    path('upload/create/', views.populate_db, name = 'create'),
    path('upload/reset/', views.reset, name = 'reset'),
    path('teamupload/', views.team_upload_file, name='teamupload'),
    path('teamupload/create/', views.team_populate_db, name = 'teamcreate'),
    path('teamupload/reset/', views.team_reset, name = 'teamreset')
]