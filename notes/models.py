from django.db import models
from django.conf import settings
from books.models import Book, Chapter, Verse
from audio.models import ChapterAudio

User = settings.AUTH_USER_MODEL

class UserNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="notes")
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True, blank=True, related_name="notes")
    verse = models.ForeignKey(Verse, on_delete=models.SET_NULL, null=True, blank=True, related_name="notes")
    page_number = models.PositiveIntegerField(null=True, blank=True, help_text="Optional, relevant for structured texts like Quran")
    note_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'verse')  # Only enforce if verse exists

    def __str__(self):
        target = self.verse or self.chapter or self.book
        return f"{self.user} note on {target}"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True, blank=True)
    verse = models.ForeignKey(Verse, on_delete=models.SET_NULL, null=True, blank=True)
    page_number = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book', 'chapter', 'verse')

    def __str__(self):
        target = self.verse or self.chapter or self.book
        return f"{self.user} bookmarked {target}"


class PlayHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="play_history")
    chapter_audio = models.ForeignKey(ChapterAudio, on_delete=models.CASCADE)
    last_position = models.FloatField(default=0.0, help_text="Seconds played")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'chapter_audio')

    def __str__(self):
        return f"{self.user} played {self.chapter_audio}"
