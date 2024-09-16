from django.contrib import admin
from django.urls import path
from videos import views


urlpatterns = [
    path('', views.video_list, name='video_list'),
    path('upload/', views.upload_video, name='upload_video'),
    path('videos/<int:video_id>/', views.video_detail, name='video_detail'),
    path('search/', views.search_subtitles, name='search_subtitles'),
    path('<int:video_id>/subtitle/<str:language>/', views.subtitle_file, name='subtitle_file'),
]