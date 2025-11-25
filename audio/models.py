from django.db import models
from books.models import Chapter, Verse
from core.models import Tenant


class Reciter(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="reciters", null=True, blank=True)
    name = models.CharField(max_length=255)
    language = models.CharField(max_length=50, default="ar")
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tenant', 'name')

    def __str__(self):
        return self.name


class ChapterAudio(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="audios")
    reciter = models.ForeignKey(Reciter, on_delete=models.CASCADE, related_name="audios")
    external_url = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to="chapter_audios/", blank=True, null=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("chapter", "reciter")

    def __str__(self):
        return f"{self.chapter.title} - {self.reciter.name}"


class AudioTimestamp(models.Model):
    chapter_audio = models.ForeignKey(ChapterAudio, on_delete=models.CASCADE, related_name="timestamps")
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE, related_name="timestamps")
    start_time = models.FloatField(help_text="Start time in seconds")
    end_time = models.FloatField(help_text="End time in seconds", null=True, blank=True)

    class Meta:
        unique_together = ("chapter_audio", "verse")

    def __str__(self):
        return f"{self.chapter_audio} - Verse {self.verse.number}"