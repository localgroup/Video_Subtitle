from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from .forms import VideoForm
from .models import Video, Subtitle
from .tasks import extract_subtitles
import os
import json


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
    video = get_object_or_404(Video, id=video_id)
    search_query = request.GET.get('search', '')
    start_time = request.GET.get('start_time', 0)
    
    # Only get subtitles for the specific video
    subtitles = video.subtitles.all()
    if search_query:
        subtitles = subtitles.filter(Q(content__icontains=search_query))
    
    # Group subtitles by language
    subtitles_by_language = {}
    languages = set()
    for subtitle in subtitles:
        if subtitle.language not in subtitles_by_language:
            subtitles_by_language[subtitle.language] = []
            languages.add(subtitle.language)
        subtitles_by_language[subtitle.language].append({
            'start_time': subtitle.start_time,
            'end_time': subtitle.end_time,
            'content': subtitle.content
        })
    
    context = {
        'video': video,
        'subtitles': subtitles,
        'search_query': search_query,
        'subtitles_json': json.dumps(subtitles_by_language),
        'languages_json': json.dumps(list(languages)),
        'start_time': start_time,
    }
    
    return render(request, 'video_detail.html', context)


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
    
    
def subtitle_file(request, video_id, language):
    video = get_object_or_404(Video, id=video_id)
    subtitles = video.subtitles.filter(language=language).order_by('start_time')
    
    vtt_content = "WEBVTT\n\n"
    for subtitle in subtitles:
        start = format_time(subtitle.start_time)
        end = format_time(subtitle.end_time)
        vtt_content += f"{start} --> {end}\n{subtitle.content}\n\n"
    
    response = HttpResponse(vtt_content, content_type='text/vtt')
    response['Content-Disposition'] = f'attachment; filename="{video.get_file_name()}_{language}.vtt"'
    return response


