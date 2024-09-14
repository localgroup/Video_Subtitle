from django.shortcuts import render, redirect
from django.conf import settings
from .forms import VideoForm
from .models import Video, Subtitle
from .tasks import extract_subtitles
import os


# Create your views here.

def search_subtitles(request):
    query = request.POST.get('q', '')
    results = Subtitle.objects.filter(content__icontains=query)
    return render(request, 'search_results.html', {'results': results, 'query': query})


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            video_path = os.path.join(settings.MEDIA_ROOT, video.file.name)
            extract_subtitles.delay(video_path, video.id)  # Use Celery task
            return redirect('video_list')
    else:
        form = VideoForm()
    return render(request, 'upload.html', {'form': form})


def video_list(request):
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})


def video_detail(request, video_id):
    video = Video.objects.get(id=video_id)
    subtitles = video.subtitles.all()
    return render(request, 'video_detail.html', {'video': video, 'subtitles': subtitles})

