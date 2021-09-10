from django.urls import path
from . import views


urlpatterns = [
    path('create_user/', views.create_user, name='user_create'),
    path('edit-profile/<str:pk>/', views.edit_profile, name='profile_edit'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user-profile/<str:pk>/', views.user_profile, name='user_profile'),
    path('user-account/', views.user_account, name='user_account'),
]
