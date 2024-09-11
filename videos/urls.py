from django.contrib import admin
from django.urls import path
from videos import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.video_list, name='video_list'),
    path('upload/', views.upload_video, name='upload_video'),
    path('videos/<int:video_id>/', views.video_detail, name='video_detail'),
    path('search/', views.search_subtitles, name='search_subtitles'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
