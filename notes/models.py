from django.db import models
from django.conf import settings
from books.models import Book, Chapter, Verse
from audio.models import ChapterAudio

User = settings.AUTH_USER_MODEL

class UserNote(models.Model):
 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE, related_name="notes")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'verse') 

    def __str__(self):
        return f"{self.user} - Verse {self.verse.number}"


class Bookmark(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True)
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book', 'chapter', 'verse')

    def __str__(self):
        if self.verse:
            return f"{self.user} bookmarked {self.verse.number}"
        elif self.chapter:
            return f"{self.user} bookmarked {self.chapter.title}"
        return f"{self.user} bookmarked {self.book.title}"


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
