import subprocess
import os
import pysrt
from django.conf import settings
from .models import Video, Subtitle
from celery import shared_task
import logging


logger = logging.getLogger(__name__)


@shared_task
def extract_subtitles(video_path, video_obj_id):
    logger.info(f"Starting subtitle extraction for video {video_obj_id}")
    video_obj = Video.objects.get(id=video_obj_id)
    output_path = os.path.join(settings.MEDIA_ROOT, 'subtitles')
    os.makedirs(output_path, exist_ok=True)
    subtitle_file = os.path.join(output_path, f'video_{video_obj_id}.srt')
    
    # Run FFmpeg to extract subtitles
    command = [
        'ffmpeg',
        '-i', video_path,
        '-map', '0:s:0',
        subtitle_file
    ]
    logger.info(f"Running FFmpeg command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        logger.error(f"FFmpeg Error: {result.stderr}")
        return
    
    if not os.path.exists(subtitle_file):
        logger.error(f"Subtitle file not created: {subtitle_file}")
        return
    
    try:
        subs = pysrt.open(subtitle_file)
    except FileNotFoundError:
        logger.error(f"Subtitle file not found: {subtitle_file}")
        return
    
    # Clear existing subtitles for this video
    video_obj.subtitles.all().delete()
    
    for sub in subs:
        start_time_seconds = (
            sub.start.hours * 3600 +
            sub.start.minutes * 60 +
            sub.start.seconds +
            sub.start.milliseconds / 1000
        )
        end_time_seconds = (
            sub.end.hours * 3600 +
            sub.end.minutes * 60 +
            sub.end.seconds +
            sub.end.milliseconds / 1000
        )
        Subtitle.objects.create(
            video=video_obj,
            language='English',
            content=sub.text,
            start_time=start_time_seconds,
            end_time=end_time_seconds
        )
    
    logger.info(f"Successfully processed subtitles for video {video_obj_id}")
    
    # Clean up the temporary subtitle file
    os.remove(subtitle_file)