from django.db import models


# Create your models here.

class Video(models.Model):
    file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
    

class Subtitle(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='subtitles')
    language = models.CharField(max_length=50)
    content = models.TextField()
    start_time = models.FloatField()  # Store start time of the subtitle in seconds

    def __str__(self):
        return f'{self.language} subtitles for {self.video}'

