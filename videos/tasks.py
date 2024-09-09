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
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    subtitle_file = os.path.join(output_path, f'{video_obj.id}.srt')
    
    # Run ccextractor
    command = ['ccextractor', video_path, '-o', subtitle_file]
    subprocess.run(command)
    
    # Parse the subtitle file and save each subtitle with its timestamp
    subs = pysrt.open(subtitle_file)
    
    for sub in subs:
        start_time_seconds = sub.start.hours * 3600 + sub.start.minutes * 60 + sub.start.seconds + sub.start.milliseconds / 1000
        Subtitle.objects.create(
            video=video_obj,
            language='English',
            content=sub.text,
            start_time=start_time_seconds
        )

