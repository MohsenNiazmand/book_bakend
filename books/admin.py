# books/admin.py
from django.contrib import admin
from .models import Book, Chapter, Verse

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'tenant', 'language', 'created_at')
    list_filter = ('tenant', 'language', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'book', 'number', 'juz')
    list_filter = ('book__tenant', 'book')
    search_fields = ('title',)

@admin.register(Verse)
class VerseAdmin(admin.ModelAdmin):
    list_display = ('number', 'chapter', 'page_number')
    list_filter = ('chapter__book__tenant', 'chapter__book', 'chapter')
    search_fields = ('text', 'translation')