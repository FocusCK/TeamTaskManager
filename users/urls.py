from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('home/', views.home, name='home'),
    path('create_team/<int:company_id>/', views.create_team, name='create_team'),
    path('assign_role/<int:team_id>/', views.assign_role, name='assign_role'),
    path('team_list/<int:company_id>/', views.team_list, name='team_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
