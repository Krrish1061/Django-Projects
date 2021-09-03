from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('create/', views.todo_create, name='todo_create'),
    path('detail/<str:pk>/', views.todo_detail, name='todo_detail'),
    path('update/<str:pk>', views.todo_update, name='todo_update'),
    path('delete/<str:pk>', views.todo_delete, name='todo_delete'),

    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
]
