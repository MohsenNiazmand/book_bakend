# notes/admin.py
from django.contrib import admin
from .models import UserNote, Bookmark, PlayHistory

@admin.register(UserNote)
class UserNoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'verse', 'created_at')
    list_filter = ('book__tenant', 'created_at')
    search_fields = ('note_text', 'user__username')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'chapter', 'verse', 'created_at')
    list_filter = ('book__tenant', 'created_at')

@admin.register(PlayHistory)
class PlayHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'chapter_audio', 'last_position', 'updated_at')
    list_filter = ('chapter_audio__chapter__book__tenant', 'updated_at')