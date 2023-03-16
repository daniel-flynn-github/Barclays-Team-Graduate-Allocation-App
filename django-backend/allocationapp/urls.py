from django.urls import path

from . import views

app_name = 'allocationapp'

urlpatterns = [
    path('', views.index, name='index'),

    # Graduate URLs
    path('graduate/cast_votes/', views.cast_votes, name='cast_votes'),
    path('graduate/vote_submitted/', views.vote_submitted, name="vote_submitted"),
    path('graduate/result_page/', views.result_page, name="result_page"),

    # Manager URLs
    path('manager/view_teams/', views.manager_view_teams, name='manager_view_teams'),
    path('manager/edit_team/<int:team_id>/', views.manager_admin_edit_team, name='manager_edit_team'),
    path('manager/edit_team/<int:team_id>/add_skill/<str:skill_name>/', views.add_new_skill, name='manager_add_skill'),
    path('manager/edit_team/<int:team_id>/add_technology/<str:tech_name>/', views.add_new_technology, name='manager_add_tech'),
    path('manager/delete_team_member/<int:user_id>/', views.delete_team_member, name='delete_team_member'),

    # Admin URLs
    path('admin/create_new_team/', views.create_new_team, name='create_new_team'),
    path('admin/create_new_user/', views.create_new_grad, name='create_new_grad'),
    path('admin/user_upload/', views.upload_file, name='upload'),
    path('admin/user_upload/create/', views.populate_db, name='create'),
    path('admin/user_upload/reset/', views.reset_graduates_managers_view, name='reset'),
    path('admin/team_upload/', views.team_upload_file, name='team_upload'),
    path('admin/team_upload/create/', views.team_populate_db, name='team_create'),
    path('admin/team_upload/reset/', views.reset_teams_view, name='team_reset'),
    path('admin/run_allocation/', views.get_allocation, name="get_allocation"),
    path('admin/portal/', views.admin_portal, name = "portal"),
    path('admin/view_teams/', views.admin_view_teams, name='admin_view_teams'),
    path('admin/edit_team/<int:team_id>/', views.manager_admin_edit_team, name='admin_edit_team'),
    path('admin/edit_team/<int:team_id>/add_skill/<str:skill_name>/', views.add_new_skill, name='admin_add_skill'),
    path('admin/edit_team/<int:team_id>/add_technology/<str:tech_name>/', views.add_new_technology, name='admin_add_tech'),
    path('admin/delete_team_member/<int:user_id>/', views.delete_team_member, name='delete_team_member'),
    path('admin/portal/reset_app/', views.reset_allocation_app, name = "reset_allocation_app"),
    path('admin/view_teams/allocation_download/', views.allocation_data_download, name = "allocation_data_download")
]
