import subprocess
import os
import pysrt
from django.conf import settings
from .models import Video, Subtitle
from celery import shared_task

@shared_task
def extract_subtitles(video_path, video_obj_id):
    video_obj = Video.objects.get(id=video_obj_id)
    output_path = os.path.join(settings.MEDIA_ROOT, 'subtitles')
    os.makedirs(output_path, exist_ok=True)
    subtitle_file = os.path.join(output_path, f'{video_obj.id}.srt')
    
    # Run FFmpeg to extract subtitles
    command = [
        'ffmpeg',
        '-i', video_path,      # Input video file
        subtitle_file          # Output subtitle file (.srt format)
    ]
    print(f"Running command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"FFmpeg Error: {result.stderr}")
        return
    
    if not os.path.exists(subtitle_file):
        print(f"Subtitle file not created: {subtitle_file}")
        return
    
    # Parse the subtitle file and save each subtitle with its timestamp
    try:
        subs = pysrt.open(subtitle_file)
    except FileNotFoundError:
        print(f"Subtitle file not found: {subtitle_file}")
        return
    
    for sub in subs:
        start_time_seconds = (
            sub.start.hours * 3600 +
            sub.start.minutes * 60 +
            sub.start.seconds +
            sub.start.milliseconds / 1000
        )
        Subtitle.objects.create(
            video=video_obj,
            language='English',
            content=sub.text,
            start_time=start_time_seconds
        )
    
    print(f"Successfully processed subtitles for video {video_obj.id}")
