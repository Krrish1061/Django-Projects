from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create-post/', views.create_post, name='create_post'),
    path('draft-post/', views.draft_post, name='draft_post'),
    path('detail-post/<str:pk>/', views.detail_post, name='detail_post'),
    path('update-post/<str:pk>/', views.update_post, name='update_post'),
    path('delete-post/<str:pk>/', views.delete_post, name='delete_post'),
    path('publish-post/<str:pk>/', views.publish_post, name='publish_post'),
    path('comment-post/<str:pk>/', views.comment_post, name='comment_post'),
    path('comment-approve/<str:pk>/',
         views.comment_approve, name='comment_approve'),
    path('comment-delete/<str:pk>/', views.comment_delete, name='comment_delete'),
]
