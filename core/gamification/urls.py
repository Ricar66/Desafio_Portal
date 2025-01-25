from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLogoutView, register

urlpatterns = [
    # Seleção de papel e autenticação
    path('', views.select_role, name='select_role'),
    path('select-role/', views.select_role, name='select_role'),
    path('login/', views.custom_login, name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register_user, name='register'),
    path('register/', register, name='register'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('broker-dashboard/', views.broker_dashboard, name='broker_dashboard'),

    # Desafios
    path('challenge/<int:challenge_id>/', views.challenge_detail, name='challenge_detail'),
    path('challenge/<int:challenge_id>/accept/', views.accept_challenge, name='accept_challenge'),
    path('create-challenge/', views.create_challenge, name='create_challenge'),
    path('assign-challenge/', views.assign_challenge, name='assign_challenge'),

    # Campanhas
    path('campanhas/', views.campaign_list, name='lista_de_campanhas'),
    path('campanhas/<int:pk>/', views.campaign_detail, name='campaign_detail'),

    # Gerenciar usuários
    path('manage-users/', views.manage_users, name='manage_users'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('add-user/', views.add_user, name='add_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('add-points/<int:score_id>/', views.add_points, name='add_points'),  # Rota para adicionar pontos
    path('delete-broker/<int:score_id>/', views.delete_broker_from_ranking, name='delete_broker'),  # Rota para excluir corretor

    # Rankings
    path('ranking/', views.ranking, name='ranking'),
    path('ranking/challenge/<int:challenge_id>/', views.challenge_ranking, name='challenge_ranking'),
    path('edit-score/<int:score_id>/', views.edit_score, name='edit_score'),
    path('delete-score/<int:score_id>/', views.delete_score, name='delete_score'),
]



