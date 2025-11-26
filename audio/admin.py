# audio/admin.py
from django.contrib import admin
from .models import Reciter, ChapterAudio, AudioTimestamp

@admin.register(Reciter)
class ReciterAdmin(admin.ModelAdmin):
    list_display = ('name', 'tenant', 'language', 'created_at')
    list_filter = ('tenant', 'language', 'created_at')
    search_fields = ('name', 'bio')

@admin.register(ChapterAudio)
class ChapterAudioAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'reciter', 'duration_seconds', 'created_at')
    list_filter = ('chapter__book__tenant', 'reciter__tenant', 'created_at')
    search_fields = ('chapter__title', 'reciter__name')

@admin.register(AudioTimestamp)
class AudioTimestampAdmin(admin.ModelAdmin):
    list_display = ('verse', 'chapter_audio', 'start_time', 'end_time')
    list_filter = ('chapter_audio__chapter__book__tenant',)