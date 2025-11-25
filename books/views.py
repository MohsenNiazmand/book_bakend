from django.shortcuts import render
from rest_framework import viewsets
from core.middleware import get_current_tenant
from .models import Book, Chapter, Verse
from .serializers import BookSerializer, ChapterSerializer, VerseSerializer

class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        tenant = get_current_tenant()
        if tenant:
            return Book.objects.filter(tenant=tenant)
        return Book.objects.none()
    
    def perform_create(self, serializer):
        tenant = get_current_tenant()
        if tenant:
            serializer.save(tenant=tenant)

class ChapterViewSet(viewsets.ModelViewSet):
    serializer_class = ChapterSerializer
    
    def get_queryset(self):
        tenant = get_current_tenant()
        if tenant:
            # Filter chapters by tenant through book relationship
            return Chapter.objects.filter(book__tenant=tenant)
        return Chapter.objects.none()
    
    def perform_create(self, serializer):
        tenant = get_current_tenant()
        if tenant:
            # Ensure book belongs to tenant
            book = serializer.validated_data.get('book')
            if book and book.tenant == tenant:
                serializer.save()

class VerseViewSet(viewsets.ModelViewSet):
    serializer_class = VerseSerializer
    
    def get_queryset(self):
        tenant = get_current_tenant()
        if tenant:
            # Filter verses by tenant through book relationship
            return Verse.objects.filter(book__tenant=tenant)
        return Verse.objects.none()
    
    def perform_create(self, serializer):
        tenant = get_current_tenant()
        if tenant:
            # Ensure book and chapter belong to tenant
            book = serializer.validated_data.get('book')
            chapter = serializer.validated_data.get('chapter')
            if book and book.tenant == tenant and chapter and chapter.book.tenant == tenant:
                serializer.save()
