from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class BandMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    cover_image = models.ImageField(upload_to='albums/', null=True, blank=True)

    def __str__(self):
        return self.title

class Song(models.Model):
    title = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="songs")
    duration = models.DurationField()
    lyrics = models.TextField(blank=True)
    youtube_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.song.title}"
